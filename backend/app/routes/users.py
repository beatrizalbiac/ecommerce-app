
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.models.users import User, UserCreate, UserPublic
# , UserUpdate
from app.dependencies import SessionDep
import time
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

logger = logging.getLogger("uvicorn")


@router.post("/auth/register", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create User object with hashed password
    db_user = User(
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        password=hashed_password,
        is_admin=False
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# @router.get("/users/", response_model=list[UserPublic])
# def read_users(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ):
#     users = session.exec(select(User).offset(offset).limit(limit)).all()
#     logger.info(f"Retrieved users: {users}")
#     return users


# @router.get("/users/{user_id}", response_model=UserPublic)
# def read_user(user_id: int, session: SessionDep):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @router.patch("/users/{user_id}", response_model=UserPublic)
# def update_user(user_id: int, user: UserUpdate, session: SessionDep):
#     user_db = session.get(User, user_id)
#     if not user_db:
#         raise HTTPException(status_code=404, detail="User not found")
#     user_data = user.model_dump(exclude_unset=True)
#     user_db.sqlmodel_update(user_data)
#     session.add(user_db)
#     session.commit()
#     session.refresh(user_db)
#     return user_db


# @router.delete("/users/{user_id}")
# def delete_user(user_id: int, session: SessionDep):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     session.delete(user)
#     session.commit()
#     return {"ok": True}
