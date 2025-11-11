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