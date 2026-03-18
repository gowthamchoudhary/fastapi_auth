from sqlalchemy import Column, Integer, String, Enum , ForeignKey,DateTime,Numeric
from sqlalchemy.orm import relationship
from database import Base
import enum
from sqlalchemy.sql import func

class Role(str, enum.Enum):
    user = "user"
    admin = "admin"
    seller = "seller"
    manager = "manager"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)        
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.user, nullable=False)
    
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

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    items = relationship("CartItem",back_populates="cart")
class CartItem(Base):
    __tablename__ = "cartitems"
    id = Column(Integer,primary_key=True,index=True)
    cart_id = Column(Integer, ForeignKey("cart.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer,nullable=False)
    cart = relationship("Cart",back_populates="items")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    total_price = Column(Integer)
    status = Column(String,default="pending")
    created_at = Column(DateTime(timezone=True),server_default=func.now())
class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer,primary_key=True,index=True)
    order_id = Column(Integer,ForeignKey("orders.id"))
    product_id = Column(Integer,ForeignKey("products.id"))
    price = Column(Numeric(10, 2))
    total_price = Column(Numeric(10, 2))


class Status(str,enum.Enum):
    pending = "pending"
    paid = "paid"
    shipping="shipping"
    delivered="delivered"