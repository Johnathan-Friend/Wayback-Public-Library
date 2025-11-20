# app/domains/items/router.py
# Gemini Assisted Code for Example (adapted for Items)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas, service
from ...db.database import get_db  # Path to your get_db dependency

# Create a new router for this domain
router = APIRouter(
    prefix="/items",   # All routes in this file start with /items
    tags=["Item"]      # Grouped under "Item" in API docs
)

# -----------------
# --- CREATE
# -----------------
@router.post(
    "/",
    response_model=schemas.ItemRead,
    status_code=status.HTTP_201_CREATED
)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new item.
    """
    new_item = service.create_item(db=db, item=item)
    return new_item

@router.get("/needs_reshelving/", response_model=List[schemas.ItemRead])
def get_items_needing_reshelving(
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of items that need reshelving.
    """
    items = service.get_items_needing_reshelving(db)
    return items



# -----------------
# --- READ (Many)
# -----------------
@router.get(
    "/",
    response_model=List[schemas.ItemRead]
)
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of items with pagination.
    """
    items = service.get_items(db, skip=skip, limit=limit)
    return items
# -----------------
# --- CHECKED OUT ITEMS
# -----------------
@router.get(
    "/checked-out",
    response_model=List[schemas.ItemWithDetailsRead],
    summary="Get all checked-out items (not damaged)"
)
def read_checked_out_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all items that are currently checked out and not damaged.
    
    Returns items with:
    - Active transaction (DateReturned is NULL)
    - IsDamaged = 0
    - Includes patron and transaction details
    """
    items = service.get_checked_out_items(db, skip=skip, limit=limit)
    return items

@router.get(
    "/available/",
    response_model=List[schemas.ItemRead]
)
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of items with pagination.
    """
    items = service.get_available_items(db, skip=skip, limit=limit)
    return items


# -----------------
# --- CHECKED IN ITEMS
# -----------------
@router.get(
    "/checked-in",
    response_model=List[schemas.ItemWithDetailsRead],
    summary="Get all checked-in items (not damaged)"
)
def read_checked_in_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all items that are currently checked in (available) and not damaged.
    
    Returns items with:
    - No active transaction (all transactions returned or never checked out)
    - IsDamaged = 0
    - Includes item details
    """
    items = service.get_checked_in_items(db, skip=skip, limit=limit)
    return items
# -----------------
# --- READ (One)
# -----------------
@router.get(
    "/{item_id}",
    response_model=schemas.ItemRead
)
def read_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single item by its ItemID.
    """
    db_item = service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item


# -----------------
# --- UPDATE
# -----------------
@router.patch(
    "/{item_id}",
    response_model=schemas.ItemRead
)
def update_item(
    item_id: int,
    item_update: schemas.ItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an item's details.
    Only the fields provided in the request body will be updated.
    """
    db_item = service.update_item(
        db,
        item_id=item_id,
        item_update=item_update
    )
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item


# -----------------
# --- DELETE
# -----------------
@router.delete(
    "/{item_id}",
    response_model=schemas.ItemRead
)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an item by its ItemID.
    Returns the deleted item's data.
    """
    db_item = service.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item

@router.post(
    "/reshelve/{item_id}")
def reshelve_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Reshelve an item by its ItemID using the stored procedure.
    """
    try:
        service.reshelve_item(item_id=item_id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reshelving item: {str(e)}"
        )
    return {"message": f"Item {item_id} reshelved successfully."}