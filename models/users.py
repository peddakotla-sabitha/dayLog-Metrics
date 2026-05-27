from database import Base
from sqlalchemy import Column, String
import uuid
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    
    id=Column(String,primary_key=True,default=lambda: str(uuid.uuid4()))
    username=Column(String,unique=True, nullable= False)
    email=Column(String,unique=True, nullable=False)
    hashed_password=Column(String,nullable=False)
    
      # 🔁 Relationships (one-to-many)
    # One user → many tasks
    tasks = relationship("Task", back_populates="user", cascade="all, delete") #back_populates must point to exact variable name on opposite model

    # One user → many expenses
    expenses = relationship("Expense", back_populates="user", cascade="all, delete")
    
