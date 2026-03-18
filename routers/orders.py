
from fastapi import APIRouter,Depends,HTTPException
from typing import List
from sqlalchemy.orm import Session
from dependencies import get_current_user
from models import Order,OrderItem,Cart,CartItem,Status
from database import get_db
from schemas import ViewOrder

router = APIRouter(prefix="/orders",tags=["orders"])


@router.post("/")
def order(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        return {"message":"Your cart is not found"}
    cartitems= db.query(CartItem).filter(CartItem.cart_id==cart.id).all()
    if not cartitems:
        return {"message":"Your cart is empty"}
    total = 0
    for item in cartitems:
        total += item.quantity * item.product.price

    
    new_order = Order(user_id=current_user.id,total_price=total,status=Status.pending)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    order_items_list = []
    for items in cartitems:
        orderitems = OrderItem(
            order_id=new_order.id,
            product_id = items.product_id,
            price= items.product.price,
            total_price = items.quantity*items.product.price,
        )
        db.add(orderitems)
        order_items_list.append(orderitems)
    db.commit()
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return order_items_list
        
@router.get("/my",response_model=List[ViewOrder])
def view_my_orders(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id==current_user.id).all()
    if orders is None:
        raise HTTPException(status_code=403,detail="Cart is not found")
    result = []
    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id==order.id).all()
        result.append(
            {
                "order_id":order.id,
                "status":order.status,
                "items":items
            }
        )
     
    return result