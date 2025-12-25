from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from .db import get_session
from .auth import get_current_user
from .models.users import User

SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[User, Depends(get_current_user)]