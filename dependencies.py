from fastapi import Depends,HTTPException
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from database import get_db
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt   
from models import User,Role,Cart,CartItem
from schemas import Token
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=['bcrypt'],deprecated = "auto")
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
def hash_password(plain:str):
    return pwd_context.hash(plain)
def verify_password(plain:str,hashed_password):
    if not pwd_context.verify(plain,hashed_password):
        return False
    return True
def create_access_token(data:dict):
    try:
        to_encode = data.copy()
        exp = datetime.now(timezone.utc)+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
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
        return payload
    except JWTError:
        raise HTTPException(status_code=404,detail="Invalid Token")
   
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401,detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=401,detail="User Not FOUND")
    return db_user

def require_role(required_roles: list):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in required_roles:
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

    