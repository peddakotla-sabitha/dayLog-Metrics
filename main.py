from fastapi import FastAPI,HTTPException, Depends
from config import APP_NAME
from schemas.task_schema import TaskCreate, TaskResponse
from schemas.expense_schema import ExpenseCreate, ExpenseResponse
from services.task_service import get_all_tasks, add_task, delete_task, update_task_status
from services.expense_service import get_all_expenses,delete_expense,add_expense
import models.task
from database import engine,Base,get_db
from sqlalchemy.orm import Session

#This line tells the Base to look at all models and create them in the DB
Base.metadata.create_all(bind=engine)


app = FastAPI(title=APP_NAME)

# --- TASKS SERVICES ---
@app.get("/",)
def home():
    return {"message": "API Running Successfully"}


@app.post("/tasks",summary= "create a new task", status_code=201 , tags= ["create a new task"])
# Added db: Session = Depends(get_db)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Pass 'db' to your service
    return add_task(db,task.title)


@app.get("/tasks", summary="getting all tasks", response_model=list[TaskResponse], status_code=200, tags=["getting all tasks"])
def fetch_tasks(db: Session=Depends(get_db)):
    
        return get_all_tasks(db)


@app.delete("/tasks/{task_id}", summary="Deleting a task", status_code=200, tags=["Deleting a task"])  #created API ENDPOINT(tasks) for deletion
def remove_task(task_id: str, db: Session=Depends(get_db)):
    try:
        delete_task(db,task_id)
        return {"message": "Task Deleted Successfully"}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail =str(e))

@app.put("/tasks/{task_id}", summary="updating the task status", tags=["updating the task status"])
def task_status_update(task_id: str, db: Session=Depends(get_db)):
    try:
        updated_task=update_task_status(db,task_id)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#EXPENSES SERVICES
@app.get("/expenses", summary = "Fetch all expenses", response_model=list[ExpenseResponse],tags=["Fetch all expenses"], status_code=200)
def fetch_expenses():
    return get_all_expenses()

@app.post("/expenses", summary= "add an expense", tags = ["add an expense"],status_code=201)
def create_expense(expense: ExpenseCreate):
    try:
        return add_expense(expense.amount,expense.category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/expenses/{expense_id}", summary = "Deleting an expense", tags=["Deleting an expense"], status_code=200)
def remove_expense(expense_id: str):
    try:
        delete_expense(expense_id)
        return {"message": "Expense Deleted Successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        

