from fastapi import FastAPI,HTTPException, Depends, APIRouter
from schemas.task_schema import TaskCreate, TaskResponse
from services.task_service import get_all_tasks, add_task, delete_task, update_task_status
from models.task import Task
from database import engine,Base,get_db
from sqlalchemy.orm import Session,joinedload
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User
from utils.auth import get_current_user


router=APIRouter()

@router.post("/tasks",summary= "create a new task", status_code=201 , tags= ["create a new task"])

# Added db: Session = Depends(get_db)
#injecting db session into routes then using it in service layer
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    # Pass 'db' to your service
    return add_task(db,task.title,current_user.id)


@router.get("/tasks", summary="getting all tasks", response_model=list[TaskResponse], status_code=200, tags=["getting all tasks"])
def fetch_tasks(status: str|None=None,search: str|None=None, skip: int=0,limit: int=5, db: Session=Depends(get_db),current_user: User=Depends(get_current_user)):
    
        return get_all_tasks(db, current_user.id,status,search,skip,limit)


@router.delete("/tasks/{task_id}", summary="Deleting a task", status_code=200, tags=["Deleting a task"])  #created API ENDPOINT(tasks) for deletion
def remove_task(task_id: str, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    try:
        delete_task(db,task_id,current_user.id)
        return {"message": "Task Deleted Successfully"}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail =str(e))

@router.put("/tasks/{task_id}", summary="updating the task status", tags=["updating the task status"])
def task_status_update(task_id: str, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    try:
        updated_task=update_task_status(db,task_id, current_user.id)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
