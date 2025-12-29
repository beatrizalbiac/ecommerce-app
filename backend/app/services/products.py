from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.products import Product

def product_exists(id: int, session: Session) -> Product:
    query = select(Product).where(Product.id == id)
    product = session.exec(query).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    return product

def check_stock (product: Product, quantity: int):
    if product.stock == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product unavailable")
    elif product.stock < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {product.stock} available")
    
def update_stock(product: Product, quantity: int, session: Session):
    stock = product.stock + quantity

    if stock < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock cannot be negative")
    
    product.stock = stock
    session.add(product)
