from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException, status

from . import models, schemas
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# Gemini caught that some of the code is not handling Pydantic v2 properly. Here is a nice example of how to do that. -Jake
def create_reservation(db: Session, reservation: schemas.ReservationCreate) -> schemas.ReservationRead:
    
    # 1. Get a dictionary of ONLY the fields the user provided.
    #    This is the modern way to handle optional fields.
    #    We use a try/except to support both Pydantic v1 (.dict) and v2 (.model_dump)
    try:
        reservation_data = reservation.model_dump(exclude_none=True)
    except AttributeError:
        reservation_data = reservation.dict(exclude_none=True) # Fallback for Pydantic v1

    # 2. Create the new database object by unpacking the dictionary.
    #    This is the correct way to create a new record.
    db_reservation = models.Reservation(**reservation_data)

    try:
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation) # Get any new data from the DB (like the ID)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error creating reservation: {str(e)}"
        )

    # 3. Return the Pydantic "Read" model.
    #    We again use try/except for Pydantic v1 (.from_orm) and v2 (.model_validate)
    try:
        return schemas.ReservationRead.model_validate(db_reservation)
    except AttributeError:
        return schemas.ReservationRead.from_orm(db_reservation) # Fallback for Pydantic v1

def get_reservations(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.ReservationRead]:
    reservations = db.query(models.Reservation).offset(skip).limit(limit).all()
    return [schemas.ReservationRead.from_orm(reservation) for reservation in reservations]

def get_reservation(db: Session, reservation_id: int) -> Optional[schemas.ReservationRead]:
    db_reservation = db.get(models.Reservation, reservation_id)
    if db_reservation is None:
        return None
    return schemas.ReservationRead.from_orm(db_reservation)

def update_reservation(db: Session, reservation_id: int, reservation_update: schemas.ReservationUpdate) -> Optional[schemas.ReservationRead]:
    db_reservation = db.get(models.Reservation, reservation_id)
    if db_reservation is None:
        return None

    for var, value in vars(reservation_update).items():
        if value is not None:
            setattr(db_reservation, var, value)

    try:
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return schemas.ReservationRead.from_orm(db_reservation)

def delete_reservation(db: Session, reservation_id: int) -> bool:
    db_reservation = db.get(models.Reservation, reservation_id)
    if db_reservation is None:
        return False

    try:
        db.delete(db_reservation)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return True