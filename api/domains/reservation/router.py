from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from . import schemas, service
from ...db.database import get_db

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@router.post("/", response_model=schemas.ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return service.create_reservation(db, reservation)

@router.get("/", response_model=List[schemas.ReservationRead])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservations = service.get_reservations(db, skip=skip, limit=limit)
    return reservations

@router.get("/{reservation_id}", response_model=schemas.ReservationRead)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = service.get_reservation(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return db_reservation

@router.patch("/{reservation_id}", response_model=schemas.ReservationRead)
def update_reservation(reservation_id: int, reservation_update: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = service.update_reservation(db, reservation_id, reservation_update)
    if db_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return db_reservation

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    success = service.delete_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return None