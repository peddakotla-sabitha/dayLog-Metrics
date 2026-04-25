from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# Engine = connection to DB
engine=create_engine(DATABASE_URL)

# Session = communication layer
SessionLocal=sessionmaker(autocommit = False, autoFlush =  False, bind = engine)

# Base class for models
Base = declarative_base()