from pydantic import BaseModel
from datetime import date
from schemas.user_schema import UserBasic

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
class ExpenseUpdate(BaseModel):
    amount: float | None = None
    category: str | None = None
class ExpenseResponseDetails(BaseModel):
    id: str
    amount:float
    category: str
    date: date
    
    user: UserBasic
    
    class Config:
        from_attributes=True
    