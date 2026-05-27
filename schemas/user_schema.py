from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(...,min_length=1)
    email: EmailStr
    password: str = Field(...,min_length=6)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserBasic(BaseModel):
    id: str
    username: str 
    class Config:
        from_attributes=True
    