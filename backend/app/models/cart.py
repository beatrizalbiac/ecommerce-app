from sqlmodel import SQLModel, Field
from typing import List

# it isn't a new table on the db, but rather smth like a temporal place to save the products the user adds to the cart

class CartItem(SQLModel):
    product_id: int = Field(gt=0) # as all my ids start from 1
    quantity: int = Field(gt=0) # it minumun needs to have more than 0

class CartValRequest(SQLModel):
    items: List[CartItem] = Field(min_length=1)

class CartItemVal(SQLModel):
    product_id: int
    title: str
    slug: str
    price_cents: int
    quantity: int
    total_price: int # cents (total price for THAT item, not the whole order)
    available_stock: int # to diferentiate it from product stock
    available: bool # wether the product can be purchased or not

class CartValResponse(SQLModel):
    items: List[CartItemVal]
    total_cents: int # total of all available items in the cart
    currency: str
    all_available: bool # true if all items are available, false if not