from typing import Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Branch(Base):
    __tablename__ = 'Branch'

    BranchID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Address: Mapped[str] = mapped_column(String(150), nullable=False)

    Employee: Mapped[list['Employee']] = relationship('Employee', back_populates='Branch_')


class Employee(Base):
    __tablename__ = 'Employee'
    __table_args__ = (
        ForeignKeyConstraint(['BranchID'], ['Branch.BranchID'], ondelete='SET NULL', onupdate='CASCADE', name='FK_Employee_Branch'),
        Index('FK_Employee_Branch', 'BranchID')
    )

    EmployeeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FirstName: Mapped[str] = mapped_column(String(50), nullable=False)
    LastName: Mapped[str] = mapped_column(String(50), nullable=False)
    BranchID: Mapped[Optional[int]] = mapped_column(Integer)
    Address: Mapped[Optional[str]] = mapped_column(String(150))
    Role: Mapped[Optional[str]] = mapped_column(String(50))

    Branch_: Mapped[Optional['Branch']] = relationship('Branch', back_populates='Employee')
