from fastapi import FastAPI
from schemas.task_schema import TaskCreate, TaskResponse
from services.task_service import get_all_tasks, add_task, delete_task, update_task_status

app = FastAPI()
@app.get("/", tags=["Tasks"])
def home():
    return {"message": "API Running Successfully"}


@app.post("/tasks",summary= "create a new task", status_code=201)
def create_task(task: TaskCreate):
    return add_task(task.title)


@app.get("/tasks", summary="getting all tasks", response_model=list[TaskResponse], status_code=200)
def fetch_tasks():
    return get_all_tasks()

@app.delete("/tasks/{task_id}", summary="Deleting a task", status_code=204)  #created API ENDPOINT(tasks) for deletion
def remove_task(task_id: str):
    return delete_task(task_id)

@app.put("/tasks/{task_id}", summary="updating the task status")
def task_status_update(task_id: str):
    return update_task_status(task_id)
