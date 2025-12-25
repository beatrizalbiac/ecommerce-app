from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserBase(SQLModel):
    name: str = Field(index=True)
    lastname: str = Field(index=True)
    email: EmailStr = Field(index=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    is_admin: bool = Field(default=False)

class UserPublic(UserBase):
    id: int
    is_admin: bool

class UserCreate(UserBase):
    password: str


# class UserUpdate(SQLModel):
#     name: str | None = None
#     age: int | None = None
#     secret_name: str | None = None