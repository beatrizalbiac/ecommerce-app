from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime, timezone, timedelta


class UserBase(SQLModel):
    name: str = Field(index=True)
    lastname: str = Field(index=True)
    email: EmailStr = Field(index=True) 

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1)) # to make it UTC+1 (The spanish time)

class UserPublic(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

class UserCreate(UserBase):
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str
