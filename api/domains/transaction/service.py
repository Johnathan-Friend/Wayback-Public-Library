from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException, status

from . import models, schemas
from ..item.models import Item
from ..item_type.models import ItemType
from ..patron.models import Patron


def get_transaction(db: Session, transaction_id: int) -> Optional[models.Transactions]:
    return db.query(models.Transactions).filter(models.Transactions.TransactionID == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Transactions]:
    return db.query(models.Transactions).offset(skip).limit(limit).all()


def get_transactions_for_patron(db: Session, patron_id: int, skip: int = 0, limit: int = 100) -> List[models.Transactions]:
    result = db.execute(text("CALL sp_PatronCurrentCheckedOutItems(:patron_id)"), {"patron_id": patron_id})
    data = result.mappings().all()
    db.commit()
    transactions = [models.Transactions(**row) for row in data]
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


def checkout_item(db: Session, patron_id: int, item_id: int):
    # Step 1: Validate patron and item existence
    patron = db.query(Patron).filter(Patron.PatronID == patron_id).first()
    item = db.query(Item).filter(Item.ItemID == item_id).first()

    if not patron or not item:
        raise HTTPException(status_code=404, detail="Patron or Item not found")

    # Step 2: Prevent damaged items from being checked out
    if item.IsDamaged and item.IsDamaged != 0:
        raise HTTPException(status_code=400, detail="Item is marked as damaged and cannot be checked out")

    # Step 3: Check if item is already checked out (DateReturned is NULL)
    active_checkout = (
        db.query(models.Transactions)
        .filter(models.Transactions.ItemID == item_id)
        .filter(models.Transactions.DateReturned.is_(None))
        .first()
    )
    if active_checkout:
        raise HTTPException(status_code=400, detail="Item is already checked out")

    # Step 4: Determine due date (use ItemType.RentalLength or default 14)
    item_details = item.ItemDetails_
    item_type = item_details.ItemType_ if item_details else None
    rental_length = getattr(item_type, "RentalLength", 14)

    # Step 5: Create new transaction
    new_transaction = models.Transactions(
        PatronID=patron.PatronID,
        ItemID=item.ItemID,
        DateStart=datetime.utcnow().date(),
        DateDue=(datetime.utcnow() + timedelta(days=rental_length)).date(),
        DateReturned=None,
        ReturnedBranchID=None
    )

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