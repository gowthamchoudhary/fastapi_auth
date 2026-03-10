from pydantic import BaseModel,EmailStr
from typing import Optional
from models import Role

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    role:Role = Role.user

class UserRead(BaseModel):
    id:int
    email:str
    role:Role

class ProductCreate(BaseModel):
    name:str
    description:Optional[str]=None
class ProductRead(BaseModel):
    owner_id:int
    name:str
    description:str
    id:int

class Token(BaseModel):
    access_token:str
    token_type:str
    