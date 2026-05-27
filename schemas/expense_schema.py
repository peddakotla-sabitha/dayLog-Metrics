from pydantic import BaseModel
from datetime import date
class ExpenseCreate(BaseModel):
    amount: float
    category: str
class ExpenseResponse(BaseModel):
    id: str
    amount:float
    category: str
    date: date
    
    class Config:
        from_attributes = True # This allows Pydantic to read SQLAlchemy objects