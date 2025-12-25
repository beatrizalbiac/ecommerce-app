from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from app.models.users import User, TokenData
from app.dependencies import SessionDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "2630e37492f20fccc39da307f2a9a4904c0dca842103887e91dfc0bc93981504"
ALGORITHM = "HS256"
# TOKEN_EXPIRED = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def authenticate_user(email: str, password: str, session):
    user = session.exec(select(User).where(User.email == email)).first()
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(email: str, id: int):
    encode = {"sub": email, "id": id}
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)