from fastapi import APIRouter, Query
from sqlmodel import select
from app.models.orders import OrderwItems, OrderCreate
from app.dependencies import SessionDep, UserDep
from fastapi import Depends, HTTPException, status
from typing import Literal

router = APIRouter()

@router.post("/orders", response_model=OrderwItems)
def create_order(order: OrderCreate, session: SessionDep, user: UserDep):
    pass