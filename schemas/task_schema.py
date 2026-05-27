from pydantic import BaseModel
from datetime import datetime
from schemas.user_schema import UserBasic

class TaskCreate(BaseModel):
    title: str
class TaskResponse(BaseModel):
    id: str
    title: str
    status: str 
    created_at: datetime  # 2. Change String to datetime
    
    user: UserBasic

    class Config:
        from_attributes = True # This allows Pydantic to read SQLAlchemy objects