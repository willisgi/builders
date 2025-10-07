from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from app.db.session import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), unique=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=False, index=True, nullable=True)
