from fastapi import APIRouter,Depends,HTTPException
from typing import List
from models import Product,Role
from schemas import ProductCreate,ProductRead,ProductUpdate
from dependencies import get_current_user,require_role
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/products",tags=["Product"])


@router.post("/create_product",response_model=ProductRead)
def create_product(product_details:ProductCreate,current_user=Depends(require_role([Role.seller,Role.admin])),db:Session=Depends(get_db)):
    
    owner_id = current_user.id
    product = Product(name=product_details.name,description=product_details.description,owner_id=owner_id,price=product_details.price,quantity=product_details.quantity)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
    
@router.post("/become-seller")
def register_seller(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    if current_user.role==Role.seller:
        raise HTTPException(status_code=400,detail="email already exits")
    current_user.role = Role.seller
    db.commit()
    return current_user
@router.get("/products",response_model=List[ProductRead])
def get_all_products(db:Session=Depends(get_db)):
    products = db.query(Product).all()
    return products
@router.get("/product/{product_id}",response_model=ProductRead)
def get_product(product_id:int,db:Session=Depends(get_db)):
    product = db.query(Product).filter(Product.id==product_id).first()
    return product
    
@router.patch("/products/{product_id}",response_model=ProductRead)
def update_product(product_id:int,product:ProductUpdate,current_user=Depends(require_role([Role.admin,Role.seller])),db:Session=Depends(get_db)):
    db_product = db.query(Product).filter(Product.id==product_id).first()
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found")
    if current_user.id != db_product.owner_id:
        raise HTTPException(status_code=403,detail="You are not allowed")
    update_data=product.dict(exclude_unset=True)
    for key,value in update_data.items():
        setattr(db_product,key,value)
    db.commit()
    db.refresh(db_product)
    return db_product
    


@router.delete("/product/{product_id}")
def delete_product(product_id:int,current_user=Depends(require_role([Role.admin,Role.seller])),db:Session=Depends(get_db)):
    db_product = db.query(Product).filter(Product.id==product_id).first()
    if not db_product:
        raise HTTPException(status_code=404,detail="product not found")
    if current_user.id!=db_product.owner_id and current_user.role!=Role.admin:
        raise HTTPException(status_code=403,detail="You are not allowed")
    db.delete(db_product)
    db.commit()
    
    return {"message":"Successfully deleted"}
    