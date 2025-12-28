from fastapi import APIRouter, Query
from sqlmodel import select
from app.models.products import Product, ProductPublic
from app.dependencies import SessionDep
from fastapi import Depends, HTTPException, status
from typing import Literal

router = APIRouter()

@router.get("/products", response_model=list[ProductPublic])
async def browse_search(session: SessionDep, 
                    q: str|None = None,
                    page: int = Query(default=1, ge=1), # the page number
                    shown: int = Query(default=9, ge=1, le=100), # products shown per page
                    sort: Literal["price_asc", "price_desc", "newest"] | None = None): # Literal is so the str is limited to those options

    skip = (page - 1) * shown
    query = select(Product)

    if q:
        query = query.where((Product.title.contains(q)) | (Product.description.contains(q))) # so it searches for not only the title but also potential key-words found on the description

    options = {
        "price_asc": Product.price_cents.asc(),
        "price_desc": Product.price_cents.desc(),
        "newest": Product.created_at.desc()
    }

    if sort in options: # it should always be in options bc of "Literal", but just to be sure
        query = query.order_by(options[sort])

    query = query.offset(skip).limit(shown)

    products = session.exec(query).all()
    return products    


# TIENE QUE IR AL FINAL
# tendrá sentido solo cuando se implemente el frontend
@router.get("/product/{slug}", response_model=ProductPublic)
def getdetails(product:Product, session:SessionDep, slug: str):
    slug = select(product).where(product.slug == slug)
    product = session.exec(slug).first()

    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Prouct not found")
    
    return product