from fastapi import APIRouter,Depends,HTTPException
from models import Product,Role
from schemas import ProductCreate,ProductRead
from dependencies import get_current_user
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/products",tags=["Product"])
# Client sends product data
# ↓
# Backend gets current_user from token
# ↓
# Check if user.role == seller
# ↓
# Create Product object
# ↓
# Set owner_id = current_user.id
# ↓
# Save product in DB
# ↓
# Return product

@router.post("/create_product",response_model=ProductRead)
def create_product(product_details:ProductCreate,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    if not current_user.role!=Role.seller:
        raise HTTPException("Not allowed")
    owner_id = current_user.id
    product = Product(name=product_details.name,description=product_details.description,owner_id=owner_id,price=product_details.price,quantity=product_details.quantity)
    
@router.post("/become-seller")
def register_seller(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    
    

    

