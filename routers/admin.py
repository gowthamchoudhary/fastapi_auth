from fastapi import APIRouter,Depends,HTTPException
from database  import get_db
from models import User,Role
from schemas import UserCreate,UserRead,UserUpdateRole
from dependencies import get_current_user,require_role
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix='/admin',tags=['Admin'])

@router.get("/get_all_sellers",response_model=List[UserRead])
def get_all_sellers(current_user=Depends(require_role([Role.admin,Role.manager])),db:Session=Depends(get_db)):
        users = db.query(User).filter(User.role==Role.seller).all()
        return users
@router.get("/get_all_managers",response_model=List[UserRead])
def get_all_managers(current_user=Depends(require_role([Role.admin])),db:Session=Depends(get_db)):
        users = db.query(User).filter(User.role==Role.manager).all()
        return users
@router.patch("/admin/users/{user_id}/make-manager",response_model=UserUpdateRole)
def make_manager(user_id:int,current_user=Depends(require_role([Role.admin])),db:Session=Depends(get_db)):
      user = db.query(User).filter(User.id==user_id).first()
      if not user:
            raise HTTPException(status_code=404,detail="User is not found")
      user.role=Role.manager
      db.commit()
      db.refresh(user)
      return user

@router.delete("/admin/seller/{user_id}")
def delete_user(user_id:int,current_user=Depends(require_role([Role.admin])),db:Session=Depends(get_db)):
      user = db.query(User).filter(User.id==user_id).first()
      if not user:
            raise HTTPException(status_code=404,detail="user not found ")
      db.delete(user)
      db.commit()
      return {"message":"Deleted the user successfully"}
@router.patch("/admin/users/seller_rights/{seller_id}",response_model=UserUpdateRole)
def remove_seller_rights(seller_id:int,db:Session=Depends(get_db),current_user=Depends(require_role([Role.admin,Role.manager]))):
      seller = db.query(User).filter(User.id==seller_id).first()
      if not seller:
            raise HTTPException(status_code=404,detail="seller not found")
      seller.role = Role.user
      db.commit()
      db.refresh(seller)
      return seller