import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL,echo=True)
sessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base = declarative_base()
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


