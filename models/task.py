from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__="tasks"
    
    
    id = Column(String, primary_key=True, default = lambda: str(uuid.uuid4()))
    title= Column(String, nullable=False)
    status=Column(String, default="pending")
    user_id= Column(String, ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime, default=datetime.now) #"call this function datetime.now whenever new row is created"
    
    
    # 🔁 Relationship (optional but useful)
    # Allows: task.user → access user object
    user = relationship("User", back_populates="tasks")
    
    # def __init__(self,title):
    #     self.id = str(uuid.uuid4())
    #     self.title=title
    #     self.status="pending"
    #     self.created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # def mark_as_completed(self):
    #     self.status="completed"
    # def to_dict(self):
    #     return {"id": self.id, "title": self.title, "status": self.status, "created_at": self.created_at}
        
    