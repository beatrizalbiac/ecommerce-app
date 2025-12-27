from sqlmodel import SQLModel, Field
from datetime import datetime, timezone, timedelta

class ProductBase(SQLModel):
    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    description: str
    price_cents: int = Field(gt=0)  # greater than
    currency: str = Field(default="EUR") # I decided to change it to euros, as that's what I'm used to, so it's easier for it to make sense when I later set some makeshift prices
    stock: int = Field(ge=0)  # greater than or equal to

class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1)) # utc+1 to keep consistency w user's created_at
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1))

class ProductPublic(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ProductCreate(ProductBase):
    pass  # bc everything is required

class ProductUpdate(SQLModel):
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    price_cents: int | None = Field(default=None, gt=0)
    currency: str | None = None
    stock: int | None = Field(default=None, ge=0)