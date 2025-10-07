from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    cashier = "cashier"

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.cashier

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True
