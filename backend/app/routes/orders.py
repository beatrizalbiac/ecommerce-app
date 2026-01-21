from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.models.orders import OrderwItems, OrderCreate, Order, Status, OrderPublic
from app.models.order_items import OrderItem
from app.dependencies import SessionDep, UserDep
from app.services.products import product_exists, check_stock

router = APIRouter()

@router.post("/orders", response_model=OrderwItems, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, session: SessionDep, user: UserDep):
    if not order.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order has no items")
    
    # just a double check so each product ordered only appears once, and it isn't separated in the instances it was added or smth
    ids = [i.product_id for i in order.items]
    if len(ids) != len(set(ids)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product duplicated")
    
    data = [] # the data of the items in the order
    cents = 0
    update = [] # the products to update after

    for i in order.items:
        product = product_exists(i.product_id, session)
        check_stock(product, i.quantity)

        total = product.price_cents * i.quantity
        cents += total

        data.append({
            "product_id": product.id,
            "product_name": product.title,
            "unit_price_cents": product.price_cents,
            "quantity": i.quantity
        })

        update.append((product, i.quantity))

    new = Order(
        user_id=user.id,
        status=Status.PENDING,
        total_cents=cents
        # currency="EUR" # it's already default
    )
    session.add(new)
    session.flush() # so it doesn't commit it and we still can make rollback if anything goes wrong

    for i in data:
        order = OrderItem(order_id=new.id, **i) # the ** is so it fills in the rest automatically, and i don't have to write the whole thing
        session.add(order)

    for product, quantity in update:
            product.stock -= quantity
            session.add(product)

    # commit everything
    try:
        session.commit()
        session.refresh(new)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create order")
    
    return new

@router.get("/orders", response_model=list[OrderwItems])
def user_all_orders(user: UserDep, session: SessionDep):
    query = (
        select(Order).where(Order.user_id == user.id).options(selectinload(Order.items)).order_by(Order.created_at.desc())
    )

    return session.exec(query).all()

@router.get("/orders/{order_id}", response_model=OrderwItems)
def get_order(order_id: int, user: UserDep, session: SessionDep):
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
     
    if order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    return order
     
    