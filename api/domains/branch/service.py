from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_branch(db: Session, branch_id: int) -> Optional[models.Branch]:
    return db.query(models.Branch).filter(models.Branch.BranchID == branch_id).first()


def get_branches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Branch]:
    return db.query(models.Branch).offset(skip).limit(limit).all()


def create_branch(db: Session, branch: schemas.BranchCreate) -> models.Branch:
    db_branch = models.Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


def update_branch(db: Session, branch_id: int, branch_update: schemas.BranchUpdate) -> Optional[models.Branch]:
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        return None

    update_data = branch_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_branch, key, value)

    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


def delete_branch(db: Session, branch_id: int) -> Optional[models.Branch]:
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        return None

    db.delete(db_branch)
    db.commit()
    return db_branch
