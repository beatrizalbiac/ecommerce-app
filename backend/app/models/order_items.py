from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .orders import Order
    from .products import Product

class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    product_name: str
    unit_price_cents: int = Field(gt=0)
    quantity: int = Field(ge=1)

class OrderItem(OrderItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order: Optional["Order"] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="order_items")

class OrderItemPublic(OrderItemBase):
    id: int

class OrderItemCreate(SQLModel):
    product_id: int
    quantity: int = Field(ge=1)