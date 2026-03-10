from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from schemas import ProductRead,ProductCreate
from models import Product,User,Role
from dependencies import get_current_user
from database import get_db

router = APIRouter(prefix="/products",tags=["products"])

@router.post("/",response_model=ProductRead)
def create_product(product:ProductCreate,current_user:User = Depends(get_current_user),db:Session = Depends(get_db)):
    db_product = Product(**product.dict(),owner_id=current_user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/",response_model=list[ProductRead])
def read_products(db:Session=Depends(get_db)):
    return db.query(Product).all()
@router.delete("/{product_id}")
def delete_product(product_id:int,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404,"Product Not Found" )
    if product.owner_id!=current_user.id or current_user.role!=Role.admin:
        raise HTTPException(403,"Not allowed")
    db.delete(product)
    db.commit()
    return {
        "detail":"product deleted"
    }