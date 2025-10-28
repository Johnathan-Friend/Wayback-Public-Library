from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas, service
from ...db.database import get_db


router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


@router.post("/", response_model=schemas.AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    new_author = service.create_author(db=db, author=author)
    return new_author


@router.get("/", response_model=List[schemas.AuthorRead])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_authors(db, skip=skip, limit=limit)


@router.get("/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = service.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return db_author


@router.patch("/{author_id}", response_model=schemas.AuthorRead)
def update_author(author_id: int, author_update: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = service.update_author(db, author_id, author_update)
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return db_author


@router.delete("/{author_id}", response_model=schemas.AuthorRead)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = service.delete_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return db_author
