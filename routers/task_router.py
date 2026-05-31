from fastapi import HTTPException, Depends, APIRouter
from schemas.task_schema import TaskCreate, TaskResponse,TaskUpdate
from services.task_service import get_all_tasks, add_task, delete_task, update_task_status,update_task,details_task
from database import get_db
from sqlalchemy.orm import Session
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

@router.put("/tasks/{task_id}/status", summary="updating the task status", tags=["updating the task status"])
def task_status_update(task_id: str, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    try:
        updated_task=update_task_status(db,task_id, current_user.id)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@router.put("/tasks/{task_id}", response_model=TaskResponse,summary="Updating the task name", status_code=200, tags=["Updating the task name"])
def task_update(task_id: str, task: TaskUpdate, db: Session=Depends(get_db), current_user: User= Depends(get_current_user)):
    try:
        updated_task=update_task(db,task_id,task.title,current_user.id)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@router.get("/tasks/details",response_model=list[TaskResponse],summary="Task details", tags=["Task details"])
def task_details(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    try:
        details=details_task(db,current_user.id)
        return details 
    except ValueError as e:
        raise HTTPException(status_code=404,details=str(e))
    

