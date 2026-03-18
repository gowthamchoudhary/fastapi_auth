from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import UserCreate,UserRead,UserUpdateRole
from models import User,Role
from dependencies import get_current_user,require_role

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/",response_model=List[UserRead])
def read_users(current_user:User=Depends(get_current_user),db:Session = Depends(get_db)):
    return db.query(User).all()
@router.delete("/{user_id}")
def delete_user(user_id:int,current_user=Depends(require_role([Role.admin])),db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    if user.id==1:
        raise HTTPException(status_code=403,detail="cannot delete main admin")
    db.delete(user)
    db.commit()
    return {"details":"User deleted"}
@router.get("/get_all_users",response_model=List[UserRead])
def get_all_users(current_user=Depends(require_role([Role.admin,Role.manager])),db:Session=Depends(get_db)):
        users = db.query(User).filter(User.role==Role.user).all()
        return users
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

@router.delete("/admin/users/{user_id}")
def delete_seller(user_id:int,current_user=Depends(require_role([Role.admin])),db:Session=Depends(get_db)):
      user = db.query(User).filter(User.id==user_id).first()
      if not user:
            raise HTTPException(status_code=404,detail="user not found ")
      db.delete(user)
      db.commit()
      return {"message":"Deleted the user successfully"}
@router.patch("/admin/users/seller_rights/{seller_id}",response_model=UserUpdateRole)
def remove_seller_rights(seller_id:int,current_user=Depends(require_role([Role.admin,Role.manager])),db:Session=Depends(get_db)):
      seller = db.query(User).filter(User.id==seller_id).first()
      if not seller:
            raise HTTPException(status_code=404,detail="seller not found")
      seller.role = Role.user
      db.commit()
      db.refresh(seller)
      return seller
