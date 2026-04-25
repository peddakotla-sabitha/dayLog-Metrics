from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str 
class TaskResponse(BaseModel):
    id: str
    title: str 
    status: str 
    created_at: str 
    