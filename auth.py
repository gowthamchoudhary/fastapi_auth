from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
from jose import JWTError,jwt
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db

from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
def verify_password(plain: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain, hashed_password)
def hash_password(plain:str):
    return pwd_context.hash(plain)
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def authenticate_user(email: str, password: str, db: Session) -> User | None:
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
