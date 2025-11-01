from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from . import schemas, service
from ...db.database import get_db
from ...domains.transaction.models import Transactions
from ...domains.item.models import Item
from ...domains.patron.models import Patron

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post("/", response_model=schemas.TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    new_transaction = service.create_transaction(db=db, transaction=transaction)
    return new_transaction


@router.get("/", response_model=List[schemas.TransactionRead])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_transactions(db, skip=skip, limit=limit)


@router.get("/{transaction_id}", response_model=schemas.TransactionRead)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = service.get_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return db_transaction


@router.get("/patron/{patron_id}", response_model=List[schemas.TransactionRead])
def read_transactions_for_patron(patron_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_transactions_for_patron(db, patron_id=patron_id, skip=skip, limit=limit)


@router.get("/patron/{patron_id}/count", response_model=int)
def read_transaction_count_for_patron(patron_id: int, db: Session = Depends(get_db)):
    return service.get_transaction_count_for_patron(db, patron_id=patron_id)


@router.patch("/{transaction_id}", response_model=schemas.TransactionRead)
def update_transaction(transaction_id: int, transaction_update: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = service.update_transaction(db, transaction_id, transaction_update)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return db_transaction


@router.delete("/{transaction_id}", response_model=schemas.TransactionRead)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = service.delete_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return db_transaction

@router.post(
    "/checkin", 
    response_model=schemas.ItemReturnResponse,
    summary="Process an Item Return"
)
def handle_item_return(
    return_request: schemas.ItemReturnRequest, 
    db: Session = Depends(get_db)
):
    try:
        return service.process_item_checkin(db=db, return_request=return_request)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/check-out-item", status_code=status.HTTP_201_CREATED)
def check_out_item(patron_id: int, item_id: int, db: Session = Depends(get_db)):
    return service.checkout_item(db=db, patron_id=patron_id, item_id=item_id)
