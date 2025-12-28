from fastapi import APIRouter, Query
from sqlmodel import select
from app.models.products import Product, ProductPublic
from app.dependencies import SessionDep
from fastapi import Depends, HTTPException, status

router = APIRouter()

@router.get("/products", response_model=list[ProductPublic])
async def browse_search(session: SessionDep, 
                    q: str|None = None,
                    page: int = Query(default=1, ge=1), # the page number
                    shown: int = Query(default=9, ge=1, le=100)): # products shown per page´

    skip = (page - 1) * shown
    query = select(Product)

    if q:
        query = query.where((Product.title.contains(q)) | (Product.description.contains(q))) # so it searches for not only the title but also potential key-words found on the description

    query = query.offset(skip).limit(shown)

    products = session.exec(query).all()
    return products    


# TIENE QUE IR AL FINAL
# cambiar esto, ya que nadie buscaria por slug -> pensar en otra forma de implementarlo
@router.get("/product/{slug}", response_model=ProductPublic)
def getdetails(product:Product, session:SessionDep, slug: str):
    slug = select(product).where(product.slug == slug)
    product = session.exec(slug).first()

    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Prouct not found")
    
    return product