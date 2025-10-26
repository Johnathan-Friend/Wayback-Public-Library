from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "Employee"

    EmployeeID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    FirstName: Mapped[str] = mapped_column(String(50), nullable=False)
    LastName: Mapped[str] = mapped_column(String(50), nullable=False)
    BranchID: Mapped[int] = mapped_column(ForeignKey("Branch.BranchID"), nullable=False)
