import uuid
from datetime import date
from sqlalchemy import Column, String, DateTime, Float,Date, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__="expenses"
    
    id=Column(String, primary_key=True,default=lambda: str(uuid.uuid4()))
    amount = Column(Float, nullable=False)
    category=Column(String, nullable=False)
    date=Column(Date, default=date.today)
    user_id= Column(String, ForeignKey("users.id"), nullable=False)
    
    #relationship
    user = relationship("User", back_populates="expenses")