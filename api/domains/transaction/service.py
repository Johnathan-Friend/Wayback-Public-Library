from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from . import models, schemas
from ..item.models import Item
from ..item_type.models import ItemType
from ..patron.models import Patron


# =====================================================
# BASIC TRANSACTION CRUD
# =====================================================

def get_transaction(db: Session, transaction_id: int) -> Optional[models.Transactions]:
    return db.query(models.Transactions).filter(models.Transactions.TransactionID == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Transactions]:
    return db.query(models.Transactions).offset(skip).limit(limit).all()


def get_active_transaction_for_item(db: Session, item_id: int) -> Optional[models.Transactions]:
    """
    Returns the most recent transaction for an item that has not been returned yet.
    """
    return (
        db.query(models.Transactions)
        .filter(models.Transactions.ItemID == item_id)
        .filter(models.Transactions.DateReturned.is_(None))  # only active checkout
        .order_by(models.Transactions.TransactionID.desc())  # latest one
        .first()
    )


def get_transactions_for_patron(db: Session, patron_id: int, skip: int = 0, limit: int = 100) -> List[schemas.PatronTransactions]:
    result = db.execute(text("CALL sp_PatronCurrentCheckedOutItems(:patron_id)"), {"patron_id": patron_id})
    data = result.mappings().all()
    db.commit()
    transactions = [schemas.PatronTransactions(**row) for row in data]
    return transactions


def get_transaction_count_for_patron(db: Session, patron_id: int) -> int:
    result = db.execute(text("CALL sp_PatronCurrentCheckedOutItemCount(:patron_id)"), {"patron_id": patron_id})
    count = result.scalar_one()
    db.commit()
    return count


def create_transaction(db: Session, transaction: schemas.TransactionCreate) -> models.Transactions:
    db_transaction = models.Transactions(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, transaction_update: schemas.TransactionUpdate) -> Optional[models.Transactions]:
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None

    update_data = transaction_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int) -> Optional[models.Transactions]:
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None

    db.delete(db_transaction)
    db.commit()
    return db_transaction


# =====================================================
# CHECK-IN (RETURN ITEM)
# =====================================================

def process_item_checkin(db: Session, return_request: schemas.ItemReturnRequest) -> schemas.ItemReturnResponse:
    """
    Calls the CheckInItem stored procedure to process an item return.
    """

    sql_call = text("""
        CALL CheckInItem(
            :p_patron_id, 
            :p_item_id, 
            :p_return_date
        )
    """)

    params = {
        "p_patron_id": return_request.patron_id,
        "p_item_id": return_request.item_id,
        "p_return_date": return_request.return_date
    }

    try:
        result_row = db.execute(sql_call, params).first()

        if not result_row:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Return failed: No result from stored procedure."
            )

        result_data = result_row._mapping

        if result_data.get('Status') == 'error':
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=result_data.get('Message', 'Error returned from stored procedure.')
            )

        try:
            response = schemas.ItemReturnResponse.model_validate(result_data)
            db.commit()
            return response
        except ValidationError as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Schema validation failed for SP response: {e}"
            )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error during item return: {e}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during check-in: {e}"
        )


# =====================================================
# CHECK-OUT (BORROW ITEM)
# =====================================================

def checkout_item(db: Session, patron_id: int, item_id: int):
    """
    Handles logic for checking out an item.
    Includes validation for item damage, duplicate checkouts,
    and applies the correct rental length based on ItemType.
    """

    # Step 1: Validate patron and item existence
    patron = db.query(Patron).filter(Patron.PatronID == patron_id).first()
    item = db.query(Item).filter(Item.ItemID == item_id).first()

    if not patron or not item:
        raise HTTPException(status_code=404, detail="Patron or Item not found")

    # Step 2: Prevent damaged items
    if item.IsDamaged and item.IsDamaged != 0:
        raise HTTPException(status_code=400, detail="Item is damaged and cannot be checked out")

    # Step 3: Ensure item is not already checked out
    active_checkout = get_active_transaction_for_item(db, item_id)
    if active_checkout:
        raise HTTPException(status_code=400, detail="Item is already checked out")

    # Step 4: Determine rental length from ItemType
    item_details = item.ItemDetails_
    item_type = item_details.ItemType_ if item_details else None
    rental_length = getattr(item_type, "RentalLength", 14)

    # Step 5: Create new transaction with correct due date
    new_transaction = models.Transactions(
        PatronID=patron.PatronID,
        ItemID=item.ItemID,
        DateStart=datetime.utcnow().date(),
        DateDue=(datetime.utcnow() + timedelta(days=rental_length)).date(),
        DateReturned=None,
        ReturnedBranchID=None
    )

    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return {
            "message": "Item checked out successfully",
            "transaction_id": new_transaction.TransactionID,
            "patron_id": patron.PatronID,
            "item_id": item.ItemID,
            "date_due": new_transaction.DateDue.isoformat()
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error during checkout: {e}")
