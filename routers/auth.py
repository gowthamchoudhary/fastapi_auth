from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from database import get_db
from schemas import UserCreate,Token
from models import User,Role
from dependencies import hash_password,authenticate_user,create_access_token


router  = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserCreate)
def register(name:str,email:str,password:str,db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email==email).first()
    if db_user:
        raise HTTPException(status_code=404,detail="email exists already")
    db_user = User(name=name,email=email,password=hash_password(password),role = Role.user)
   
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token(data={"sub"=name,"role":Role.user.value})
@router.post("/token",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    db_user=authenticate_user(form_data.username,form_data.password,db)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User Not Found")

    