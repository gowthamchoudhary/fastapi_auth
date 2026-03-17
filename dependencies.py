from fastapi import Depends,HTTPException
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from database import get_db
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt   
from models import User,Token,Role,Cart,CartItem

pwd_context = CryptContext(schemes=['bcrypt'],deprecated = "auto")
load_dotenv()
SECRET_KEY = os.getenv('DATABASE_URL')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
def hash_password(plain:str):
    return pwd_context.hash(plain)
def verify_password(plain:str,hashed_password):
    if not pwd_context.verify(plain,hashed_password):
        return False
    return True
def create_access_token(data:dict):
    try:
        to_encode = data.copy()
        exp = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp":exp})
        return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    except JWTError as e:
        return {"error_message":e}
def authenticate_user(email:str,password:str,db:Session):
    db_user = db.query(User).filter(User.email==email).first()
    if not db_user or not verify_password(password,db_user.hashed_password):
        return HTTPException(status_code=404,detail="Invalid credentials")
    return db_user

def verify_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=404,detail="Invalid Token")
   
def get_current_user(token:Token,db:Session):
    payload = verify_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=404,detail="No user Found")
    db_user = db.query(User).filter(User.id==user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User Not FOUND")
    return db_user

def require_role(required_role:list):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role!=required_role:
            raise HTTPException(status_code=403,detail="You dont have enough permission to take the action")
        return current_user
    return role_checker

def add_to_cart(product_id, cart_id, quantity, db: Session):
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id
    ).first()

    if cart_item:
       
        cart_item.quantity += quantity
    else:
       
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )
    
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item



def create_cart(user_id,db:Session):
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

    