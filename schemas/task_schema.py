from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str 
class TaskResponse(BaseModel):
    id: str
    title: str
    status: str 
    created_at: datetime  # 2. Change String to datetime

    class Config:
        from_attributes = True # This allows Pydantic to read SQLAlchemy objects