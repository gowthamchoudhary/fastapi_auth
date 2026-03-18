from fastapi import FastAPI
from routers import auth,products,users,admin,cart,orders
import uvicorn

app = FastAPI(title="RBAC")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(admin.router)
app.include_router(cart.router)
app.include_router(orders.router)


if __name__ == "__main__":
        uvicorn.run("main:app",reload=True)

# At the bottom of main.py or in a separate init_db.py
from database import engine
from models import Base

def init_db(drop_all=False):
    if drop_all:
        Base.metadata.drop_all(bind=engine)
        print("Dropped all tables")
    Base.metadata.create_all(bind=engine)
    print("Created all tables")

if __name__ == "__main__":
    init_db(drop_all=True)