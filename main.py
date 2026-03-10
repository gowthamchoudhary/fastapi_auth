from fastapi import FastAPI
from routers import auth,products,users
import uvicorn

app = FastAPI(title="RBAC")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)


if __name__ == "__main__":
        uvicorn.run("main:app",reload=True)

# At the bottom of main.py or in a separate init_db.py
from database import engine
from models import Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()