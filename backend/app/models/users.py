from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from datetime import datetime, timezone, timedelta
if TYPE_CHECKING:
    from .orders import Order

class UserBase(SQLModel):
    name: str = Field(index=True)
    lastname: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True) # w unique it checks 4 me if it's dupped, but the error is ugly and out of my control

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1)) # to make it UTC+1 (The spanish time)
    orders: List["Order"] = Relationship(back_populates="user")

class UserPublic(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

class UserCreate(UserBase):
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str
