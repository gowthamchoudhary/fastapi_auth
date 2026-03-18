from pydantic import BaseModel,EmailStr
from typing import Optional,List
from models import Role

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    

class UserRead(BaseModel):
    id:int
    email:str
    role:Role

class ProductCreate(BaseModel):
    name:str
    price:int
    quantity:int
    description:Optional[str]=None
class ProductRead(BaseModel):
    owner_id:int
    name:str
    price:int
    quantity:int
    description:str
    id:int

class Token(BaseModel):
    access_token:str
    token_type:str
class ProductUpdate(BaseModel):
    name:Optional[str]
    price:Optional[int]
    quantity:Optional[int]
    description:Optional[str]

class UserUpdateRole(BaseModel):
    name:Optional[str]
    role:Optional[str] 
   
class AddToCart(BaseModel):
    productId:int
    quantity:int


class CartItemSchema(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float

class ViewCart(BaseModel):
    cart_id: int
    items: List[CartItemSchema]
    total_items: int
    total_price: float
    message: Optional[str] = None
class ViewOrder(BaseModel):
    order_id:int
    status:str
    total_price: float
    items: List[dict] = []

