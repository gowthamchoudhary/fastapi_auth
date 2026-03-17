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
    hashed_password = hash_password(password)
    db_user = User(name=name,email=email,hash_password=hashed_password,role=Role.user,products=None)
      
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
   
    token = create_access_token(data={"sub":db_user.id,"role":db_user.role.value})
    return {"access_token":token,"token_type":"Bearer"}
@router.post("/token",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    db_user=authenticate_user(form_data.username,form_data.password,db)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User Not Found")
    token = create_access_token(data={"sub":db_user.id,"password":hash_password(form_data.password),"role":db_user.role.value})
    return {"access_token":token,"token_type":"Bearer"}
       