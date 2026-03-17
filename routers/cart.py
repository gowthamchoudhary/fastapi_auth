from fastapi import APIRouter,Depends,HTTPException
from models import Product,Role,Cart,User,CartItem  
from schemas import ProductCreate,ProductRead,ProductUpdate,AddToCart,ViewCart,CartItemSchema
from dependencies import get_current_user,require_role,create_cart,add_to_cart
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cart",tags=["cart"])


@router.post("/items",response_model=AddToCart)
def addtocart(product_id:int,quantity:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    current_user_cart=db.query(Cart).filter(Cart.user_id==current_user.id).first()
    if not current_user_cart:
        cart  = create_cart(current_user.id)
        
    
    add_to_cart(product_id,current_user_cart.id,quantity,db)
    return {"message":"Items is added to cart"}

@router.get("/cart",response_model=ViewCart)
def viewCart(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id==current_user.id).first()
    if not cart:
        return {
            "cart_id":0,
            "items":[],
            "total_items":0,
            "message":"cart is empty"
        }
    cartitems = db.query(CartItem).filter(CartItem.cart_id==cart.id).all()
    items = []
    for item in cartitems:
        items.append({
            "product_id":item.product_id,
            "product_name":item.product.name,
            "quantity":item.quantity,
            "description":item.product.description,
            "price":item.product.price,
            "stock_available":item.product.quantity
        })
    return {
        "cart_id":cart.id,
        "items":items,
        "total_items":len(items),
        "total_price":sum(item["price"]*item["quantity"] for  item in items)
    }

@router.patch("/items/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        return {"message": "Cart doesn't exist"}

    cartitem = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_id
    ).first()

    if not cartitem:
        return {"message": "Product not found in cart"}

    cartitem.quantity = quantity  # ✅ correct field

    db.commit()
    db.refresh(cartitem)

    return {
        "message": "Successfully updated",
        "item_id": cartitem.product_id,
        "quantity": cartitem.quantity
    }

@router.delete("/items/{item_id}")
def delete_product(item_id:int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id==current_user.id).first()
    if not cart:
        return {"message":"Cart doesnt exists"}
    cartitem = db.query(CartItem).filter(CartItem.cart_id==cart.id,CartItem.product_id==item_id).first()
    db.delete(cartitem)
    db.commit()
    return {"message":"successfully deleted"}