from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from database import get_db
from schemas import UserCreate,Token
from models import User,Role
from dependencies import hash_password,authenticate_user,create_access_token
from schemas import UserCreate,Token


router  = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="email exists already")

    hashed_password = hash_password(user_data.password)

    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=Role.user
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token(data={
        "sub": db_user.id,
        "role": db_user.role.value
    })

    return {"access_token": token, "token_type": "Bearer"}
@router.post("/token",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    db_user=authenticate_user(form_data.username,form_data.password,db)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User Not Found")
    token = create_access_token(data={
        "sub": str(db_user.id),
        "role": db_user.role
    })
    return {"access_token":token,"token_type":"Bearer"}
       