# app/domains/items/service.py

from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import text

# -----------------
# --- READ (One)
# -----------------
def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """
    Get a single item by its ItemID.
    """
    return db.query(models.Item).filter(models.Item.ItemID == item_id).first()


# -----------------
# --- READ (Many)
# -----------------
def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """
    Get a list of all items with pagination.
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


# -----------------
# --- CREATE
# -----------------
def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    """
    Create a new item in the database.
    """
    db_item = models.Item(**item.model_dump())

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# -----------------
# --- UPDATE
# -----------------
def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate) -> Optional[models.Item]:
    """
    Update an existing item's information.
    """
    db_item = get_item(db, item_id)

    if not db_item:
        return None  # The item doesn't exist

    update_data = item_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# -----------------
# --- DELETE
# -----------------
def delete_item(db: Session, item_id: int) -> Optional[models.Item]:
    """
    Delete an item from the database.
    """
    db_item = get_item(db, item_id)

    if not db_item:
        return None  # The item doesn't exist

    db.delete(db_item)
    db.commit()
    return db_item


# -----------------
# --- CHECKED OUT ITEMS (Not Damaged)
# -----------------
def get_checked_out_items(db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get all items that are currently checked out and not damaged.
    An item is checked out if it has an active transaction (DateReturned is NULL).
    """
    from ..transaction.models import Transactions
    from ..item_details.models import ItemDetails
    from ..item_type.models import ItemType
    from ..patron.models import Patron
    
    # Query items that:
    # 1. Are NOT damaged (IsDamaged = 0)
    # 2. Have an active transaction (DateReturned IS NULL)
    results = (
        db.query(
            models.Item.ItemID,
            models.Item.ISBN,
            models.Item.BranchID,
            models.Item.IsDamaged,
            ItemDetails.Title,
            ItemType.TypeName.label('ItemTypeName'),
            Transactions.TransactionID,
            Transactions.PatronID,
            Transactions.DateStart,
            Transactions.DateDue,
            Patron.FirstName,
            Patron.LastName
        )
        .join(Transactions, models.Item.ItemID == Transactions.ItemID)
        .join(ItemDetails, models.Item.ISBN == ItemDetails.ISBN)
        .join(ItemType, ItemDetails.ItemTypeID == ItemType.ItemTypeID)
        .join(Patron, Transactions.PatronID == Patron.PatronID)
        .filter(models.Item.IsDamaged == 0)  # Not damaged
        .filter(Transactions.DateReturned.is_(None))  # Not returned yet (checked out)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Convert to list of dictionaries
    items_list = []
    for row in results:
        items_list.append({
            "ItemID": row.ItemID,
            "ISBN": row.ISBN,
            "BranchID": row.BranchID,
            "IsDamaged": row.IsDamaged,
            "Title": row.Title,
            "ItemTypeName": row.ItemTypeName,
            "TransactionID": row.TransactionID,
            "PatronID": row.PatronID,
            "PatronName": f"{row.FirstName} {row.LastName}",
            "DateStart": row.DateStart,
            "DateDue": row.DateDue
        })
    
    return items_list


# -----------------
# --- CHECKED IN ITEMS (Not Damaged)
# -----------------
def get_checked_in_items(db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get all items that are currently checked in (available) and not damaged.
    An item is checked in if it has NO active transaction (all transactions have DateReturned set).
    """
    from ..transaction.models import Transactions
    from ..item_details.models import ItemDetails
    from ..item_type.models import ItemType
    
    # Subquery to find items with active checkouts
    active_checkouts_subquery = (
        db.query(Transactions.ItemID)
        .filter(Transactions.DateReturned.is_(None))
        .subquery()
    )
    
    # Query items that:
    # 1. Are NOT damaged (IsDamaged = 0)
    # 2. Do NOT have an active transaction (ItemID not in active checkouts)
    results = (
        db.query(
            models.Item.ItemID,
            models.Item.ISBN,
            models.Item.BranchID,
            models.Item.IsDamaged,
            ItemDetails.Title,
            ItemType.TypeName.label('ItemTypeName')
        )
        .join(ItemDetails, models.Item.ISBN == ItemDetails.ISBN)
        .join(ItemType, ItemDetails.ItemTypeID == ItemType.ItemTypeID)
        .filter(models.Item.IsDamaged == 0)  # Not damaged
        .filter(~models.Item.ItemID.in_(active_checkouts_subquery))  # Not checked out
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Convert to list of dictionaries
    items_list = []
    for row in results:
        items_list.append({
            "ItemID": row.ItemID,
            "ISBN": row.ISBN,
            "BranchID": row.BranchID,
            "IsDamaged": row.IsDamaged,
            "Title": row.Title,
            "ItemTypeName": row.ItemTypeName,
            "TransactionID": None,
            "PatronID": None,
            "PatronName": None,
            "DateStart": None,
            "DateDue": None
        })
    
    return items_list


# -----------------
# --- GET ITEMS NEEDING RESHELVING
# -----------------
def get_items_needing_reshelving(db: Session) -> List[models.Item]:
    """
    Get a list of items that need reshelving.
    """
    return db.query(models.Item).filter(models.Item.Status == 'Needs Reshelving').all()


# -----------------
# --- RESHELVE ITEM
# -----------------
#Gemini fixed my original poor code for calling a stored procedure. -Jake
def reshelve_item(item_id: int, db: Session):
    """
    Executes the 'ReshelveItem' stored procedure for a given ItemID.

    This endpoint will update an item's status from 'Needs Reshelving' 
    to 'Available'.
    """
    try:
        # 1. Prepare the raw SQL to call the stored procedure
        # We use text() from SQLAlchemy and named parameters to prevent SQL injection
        sql_query = text("CALL ReshelveItem(:p_item_id)")
        
        # 2. Execute the procedure and pass the item_id
        result_proxy = db.execute(sql_query, {"p_item_id": item_id})
        
        # 3. Fetch the single result row (our SP always returns one row)
        result = result_proxy.fetchone()

        if not result:
            # This should not happen if the SP is correct, but it's good defense.
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Stored procedure did not return a result."
            )

        # 4. The SP performs an UPDATE, so we must commit the transaction.
        # We commit *after* fetching, but *before* checking the logical result.
        db.commit()

        # 5. Handle the logical outcome from the stored procedure
        if result.Status == 'success':
            # Success! Return a 200 OK with the success message.
            return {"status": "success", "message": result.Message}
        
        else:
            # The SP returned a 'error' status. Map it to a proper HTTP error.
            if "Invalid ItemID" in result.Message:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result.Message
                )
            elif "cannot be reshelved" in result.Message:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=result.Message
                )
            else:
                # Fallback for any other 'error' message from the SP
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.Message
                )

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions we created so FastAPI can handle them
        raise http_exc
    except Exception as e:
        # If any other database error occurs (e.g., connection lost), rollback
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected database error occurred: {str(e)}"
        )