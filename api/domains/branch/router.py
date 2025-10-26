from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas, service
from ...db.database import get_db


router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)


@router.post("/", response_model=schemas.BranchRead, status_code=status.HTTP_201_CREATED)
def create_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    new_branch = service.create_branch(db=db, branch=branch)
    return new_branch


@router.get("/", response_model=List[schemas.BranchRead])
def read_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_branches(db, skip=skip, limit=limit)


@router.get("/{branch_id}", response_model=schemas.BranchRead)
def read_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = service.get_branch(db, branch_id)
    if db_branch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return db_branch


@router.patch("/{branch_id}", response_model=schemas.BranchRead)
def update_branch(branch_id: int, branch_update: schemas.BranchUpdate, db: Session = Depends(get_db)):
    db_branch = service.update_branch(db, branch_id, branch_update)
    if db_branch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return db_branch


@router.delete("/{branch_id}", response_model=schemas.BranchRead)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = service.delete_branch(db, branch_id)
    if db_branch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return db_branch
