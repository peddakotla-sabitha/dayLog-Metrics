from utils.file_handler import read_json, write_json
from config import DATA_FILE
from models.task import Task
from sqlalchemy.orm import Session, joinedload



# 1. GET ALL TASKS
def get_all_tasks(db: Session,user_id:str, status: str|None=None, search: str|None=None,skip: int=0,limit: int=5):
    query=db.query(Task).filter(Task.user_id==user_id)
    
    if status:
        query=query.filter(Task.status==status)
    if search:
        query=query.filter(Task.title.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

    # This is equivalent to "SELECT * FROM tasks"
    #return db.query(Task).filter(Task.user_id==user_id).all()
    



# 2. ADD A NEW TASK
def add_task(db: Session, title: str, user_id: str):
    
    #creating an object to task class
    new_task=Task(title = title, user_id=user_id) 
    
    # Add to the "Pending" list (The Shopping Cart)
    db.add(new_task)  #object relati onal mapping
    
    # Save permanently to Postgres (The Checkout)
    db.commit()
    # Refresh to get the ID and default status from the DB
    db.refresh(new_task)
    return new_task


# 3. DELETE A TASK
def delete_task(db: Session, task_id: str, user_id: str):
    # Find the task first
    task=db.query(Task).filter(Task.id==task_id, Task.user_id==user_id).first()
    if not task:
        raise ValueError(f"Task {task_id} not found or not authorized")
    db.delete(task)
    db.commit()

# 4. UPDATE STATUS
def update_task_status(db: Session, task_id: str,user_id: str):
    task=db.query(Task).filter(Task.id==task_id, Task.user_id==user_id).first()
    
    if not task:
        raise ValueError(f"Task {task_id}not found or not authorized")
    task.status="completed" if task.status=="pending" else "pending"
    
    db.commit()
    db.refresh(task)
    return task

#5.UPDATE TASK TITLE
def update_task(db:Session, task_id: str, new_title: str, user_id: str):
    task=db.query(Task).options(joinedload(Task.user)).filter(Task.id==task_id, Task.user_id==user_id).first()
    if not task:
        raise ValueError(f"Task not found")
    if task.title==new_title:
        raise ValueError("New title is same as current title")
    task.title = new_title
    db.commit()
    db.refresh(task)
    return task


def details_task(db: Session, user_id: str):
    tasks=db.query(Task).options(joinedload(Task.user)).filter(Task.user_id==user_id).all()
    if not tasks:
        raise ValueError("Tasks not found")
    return tasks
    
    
    
    