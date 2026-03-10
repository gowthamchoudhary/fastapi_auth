from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import UserCreate,UserRead
from models import User
from dependencies import get_current_user,get_current_admin

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/",response_model=List[UserRead])
def read_users(current_user:User=Depends(get_current_user),db:Session = Depends(get_db)):
    return db.query(User).all()
@router.delete("/{user_id}",dependencies=[Depends(get_current_admin)])
def delete_user(user_id:int,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(404,"User not found")
    if user.id==1:
        raise HTTPException(403,"cannot delete main admin")
    db.delete(user)
    db.commit()
    return {"details":"User deleted"}
