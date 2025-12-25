
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
# from sqlmodel import Session, select
from app.models.users import User, UserCreate, UserPublic, Token
from app.dependencies import SessionDep, UserDep
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import get_password_hash, authenticate_user, create_access_token

router = APIRouter()

logger = logging.getLogger("uvicorn")


@router.post("/auth/register", response_model=UserPublic)
def register(user: UserCreate, session: SessionDep):

    # CONSIDER CHECKING FOR DUPED EMAILS
    
    db_user = User(
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        password=get_password_hash(user.password),
        is_admin=False
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/auth/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(form_data.username, form_data.password, session) # it will show as "username" but there goes the email
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    token = create_access_token(user.email, user.id)

    return {"access_token": token, "token_type": "bearer"}

@router.get("/auth/me", response_model=UserPublic)
async def user(user: UserDep):
    return user

# THINGS TO ADD IF THERE'S EXTRA TIME

# ERASE USER

# UPDATE USER

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
