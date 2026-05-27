from fastapi import FastAPI 
from config import APP_NAME
from routers.task_router import router as task_router
from routers.expense_router import router as expense_router
from routers.user_router import router as user_router



#This line tells the Base to look at all models and create them in the DB
#Base.metadata.create_all(bind=engine)   --Since you already use Alembic:


app = FastAPI(title=APP_NAME)
app.include_router(task_router)
app.include_router(expense_router)
app.include_router(user_router)

@app.get("/",)
def home():
    return {"message": "API Running Successfully"}


    