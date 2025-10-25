# app/domains/patrons/service.py

from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# -----------------
# --- READ (One)
# -----------------
def get_patron(db: Session, patron_id: int) -> Optional[models.Patron]:
    """
    Get a single patron by their PatronID.
    """
    return db.query(models.Patron).filter(models.Patron.PatronID == patron_id).first()

# -----------------
# --- READ (Many)
# -----------------
def get_patrons(db: Session, skip: int = 0, limit: int = 100) -> List[models.Patron]:
    """
    Get a list of all patrons with pagination.
    """
    return db.query(models.Patron).offset(skip).limit(limit).all()

# -----------------
# --- CREATE
# -----------------
def create_patron(db: Session, patron: schemas.PatronCreate) -> models.Patron:
    """
    Create a new patron in the database.
    """
    # Convert Pydantic schema to a dictionary and unpack it
    db_patron = models.Patron(**patron.model_dump())
    
    db.add(db_patron)
    db.commit()
    db.refresh(db_patron)
    return db_patron

# -----------------
# --- UPDATE
# -----------------
def update_patron(db: Session, patron_id: int, patron_update: schemas.PatronUpdate) -> Optional[models.Patron]:
    """
    Update an existing patron's information.
    """
    db_patron = get_patron(db, patron_id)
    
    if not db_patron:
        return None # The patron doesn't exist

    # Get the update data as a dict, excluding any fields that weren't set (for PATCH)
    update_data = patron_update.model_dump(exclude_unset=True)

    # Loop through the update data and set the new values
    for key, value in update_data.items():
        setattr(db_patron, key, value)

    db.add(db_patron)
    db.commit()
    db.refresh(db_patron)
    return db_patron

# -----------------
# --- DELETE
# -----------------
def delete_patron(db: Session, patron_id: int) -> Optional[models.Patron]:
    """
    Delete a patron from the database.
    """
    db_patron = get_patron(db, patron_id)

    if not db_patron:
        return None # The patron doesn't exist

    db.delete(db_patron)
    db.commit()
    return db_patron