from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

class Role(str, enum.Enum):
    user = "user"
    admin = "admin"
    seller = "seller"
    manager = "manager"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)              # usually required
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(Role), default=Role.user, nullable=False)
    
    products = relationship("Product", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)    
    quantity=Column(Integer,nullable=False )
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")