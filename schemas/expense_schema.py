from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    amount: float
    category: str
class ExpenseResponse(BaseModel):
    id: str
    amount:float
    category: str
    date: str