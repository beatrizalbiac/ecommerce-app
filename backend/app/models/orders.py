from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, timezone, timedelta
from enum import Enum
if TYPE_CHECKING:
    from .users import User
    from .order_items import OrderItem, OrderItemPublic

from .order_items import OrderItemPublic, OrderItemCreate

class Status(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class OrderBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    status: Status = Field(default=Status.PENDING)
    total_cents: int =  Field(gt=0)
    currency: str = Field(default="EUR")

class Order(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1)) # utc+1
    user: Optional["User"] = Relationship(back_populates="orders") # it doesn't work with User | None bc this is part of SQLAlchemy, which is older than SQLModel, and doesn't get "newer" ways or smth
    items: List["OrderItem"] = Relationship(back_populates="order")
    
class OrderPublic(OrderBase):
    id: int
    created_at: datetime

class OrderwItems(OrderPublic):
    items: List[OrderItemPublic]

class OrderCreate(SQLModel):
    items: List[OrderItemCreate] = Field(min_length=1)