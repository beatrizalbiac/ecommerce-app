from fastapi import APIRouter, HTTPException
from app.models.cart import CartItemVal, CartValRequest, CartValResponse
from app.dependencies import SessionDep
from app.services.products import product_exists, check_stock

router = APIRouter()

@router.post("/checkout/validate", response_model=CartValResponse)
def validate(request: CartValRequest, session: SessionDep):
    validated = []
    cents = 0
    all_available = True

    for i in request.items:
        try:
            product = product_exists(i.product_id, session)

            try:
                check_stock(product, i.quantity)
                available = True
            except HTTPException:
                available = False
                all_available = False
            
            total = product.price_cents * i.quantity
            if available:
                cents += total

            val = CartItemVal( # val = and item validated
                product_id=product.id,
                title=product.title,
                slug=product.slug,
                price_cents=product.price_cents,
                quantity=i.quantity,
                total_price=total,
                available_stock=product.stock,
                available=available
            )

            validated.append(val)

        except HTTPException:
            all_available = False
        
    return CartValResponse(
        items=validated,
        total_cents=cents,
        currency="EUR",
        all_available=all_available
    )