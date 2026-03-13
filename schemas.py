from pydantic import BaseModel,EmailStr
from typing import Optional
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
    price:str
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
