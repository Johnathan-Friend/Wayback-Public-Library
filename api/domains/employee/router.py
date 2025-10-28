from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas, service
from ...db.database import get_db


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = service.create_employee(db=db, employee=employee)
    return new_employee


@router.get("/", response_model=List[schemas.EmployeeRead])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_employees(db, skip=skip, limit=limit)


@router.get("/{employee_id}", response_model=schemas.EmployeeRead)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = service.get_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return db_employee


@router.patch("/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = service.update_employee(db, employee_id, employee_update)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return db_employee


@router.delete("/{employee_id}", response_model=schemas.EmployeeRead)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = service.delete_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return db_employee
