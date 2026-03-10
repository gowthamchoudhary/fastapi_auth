from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from models import User,Role
from fastapi import Depends,HTTPException
from database import get_db
from auth import SECRET_KEY,ALGORITHM
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401,detail="could not validate credentials")
    except (JWTError,ValueError):
        return HTTPException(status_code=401,detail="could not validate credentials")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=401,detail="Couldnt Validate the credentials")
    return db_user
def require_role(required_role:str):
    def role_checker(current_user:User=Depends(get_current_user)):
        if current_user.role!=required_role and current_user.role != Role.admin:
            raise HTTPException(status_code=403,detail="Not enough permission")
        return current_user
    return role_checker 

get_current_admin = require_role("admin")
