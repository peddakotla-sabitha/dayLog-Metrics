from utils.file_handler import read_json, write_json
from config import DATA_FILE
from models.task import Task
from sqlalchemy.orm import Session



# 1. GET ALL TASKS
def get_all_tasks(db: Session):
    
    # This is equivalent to "SELECT * FROM tasks"
    return db.query(Task).all()
    



# 2. ADD A NEW TASK
def add_task(db: Session, title: str):
    
    #creating an object to task class
    new_task=Task(title = title) 
    
    # Add to the "Pending" list (The Shopping Cart)
    db.add(new_task)  #object relational mapping
    
    # Save permanently to Postgres (The Checkout)
    db.commit()
    # Refresh to get the ID and default status from the DB
    db.refresh(new_task)
    return new_task


# 3. DELETE A TASK
def delete_task(db: Session, task_id: str):
    # Find the task first
    task=db.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise ValueError(f"Task with id {task_id} not found")
    db.delete(task)
    db.commit()

# 4. UPDATE STATUS
def update_task_status(db: Session, task_id: str):
    task=db.query(Task).filter(Task.id==task_id).first()
    
    if not task:
        raise ValueError(f"Task with ID {task_id} not found")
    task.status="completed" if task.status=="pending" else "pending"
    
    db.commit()
    db.refresh(task)
    return task

    
    
    