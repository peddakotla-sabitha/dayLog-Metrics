from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# Engine = connection to DB
engine=create_engine(DATABASE_URL)

# Session = communication layer
SessionLocal=sessionmaker(autocommit = False, autoflush =  False, bind = engine)

# Base class for models
Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()