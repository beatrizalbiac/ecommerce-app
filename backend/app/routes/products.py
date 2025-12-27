from fastapi import APIRouter, Query
from sqlmodel import select
from app.models.products import Product, ProductPublic
from app.dependencies import SessionDep
from fastapi import Depends, HTTPException, status

router = APIRouter()

@router.get("/products", response_model=list[ProductPublic])
async def returnall(product: Product, session: SessionDep, 
                    q: str|None = None,
                    page: int = Query(default=1, ge=1), # the page number
                    shown: int = Query(default=9, ge=1, le=100)): # products shown per page´

    skip = (page - 1) * shown
    query = select(product)

    if q:
        query = query.where(Product.title.contains(q))
    query = query.offset(skip).limit(shown)

    products = session.exec(query).all()
    return products    


# TIENE QUE IR AL FINAL
@router.get("/product/{slug}", response_model=ProductPublic)
def getdetails(product:Product, session:SessionDep, slug: str):
    slug = select(product).where(product.slug == slug)
    product = session.exec(slug).first()

    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Prouct not found")
    
    return product