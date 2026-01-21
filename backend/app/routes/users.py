
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.models.users import User, UserCreate, UserPublic, Token
from app.dependencies import SessionDep, UserDep
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import get_password_hash, authenticate_user, create_access_token

router = APIRouter()

logger = logging.getLogger("uvicorn")


@router.post("/auth/register", response_model=UserPublic)
def register(user: UserCreate, session: SessionDep):

    # if it were a real web, It should check wether the emails exist or not, but as i'm not using google's API nor anything alike there's no need to :)
    # but then still have to check if the email is dupped
    exists = session.exec(select(User).where(User.email == user.email)).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
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