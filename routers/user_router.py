from fastapi import HTTPException, Depends, APIRouter
from schemas.user_schema import UserCreate
from database import engine,Base,get_db
from sqlalchemy.orm import Session
from services.user_service import create_user,authenticate_user
from utils.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User




router=APIRouter()
#User services

#user registration
@router.post("/register", summary="Register new users", tags=["Register"],status_code=201)
def register_user(user: UserCreate, db: Session=Depends(get_db)):
    try:
        return create_user(db,user.username, user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


#Authenticating user

@router.post("/login", summary="Log in", tags=["Log in"])
def auth_user(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Swagger sends form-data (username + password)
    db: Session = Depends(get_db)                      # DB session injected
):
    try:
        # OAuth2 uses "username" field → we treat it as EMAIL
        email = form_data.username
        password = form_data.password

        # Step 1: Validate user credentials (email + password)
        user = authenticate_user(db, email, password)

        # Step 2: Create JWT token
        # "sub" (subject) → stores user identity (we use user.id)
        access_token = create_access_token({
            "sub": str(user.id)
        })

        # Step 3: Return token in standard OAuth format
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except ValueError as e:
        # If authentication fails → return 401 Unauthorized
        raise HTTPException(status_code=401, detail=str(e))
    
    

@router.get("/user-with-expenses")
def users_with_expenses(db:Session=Depends(get_db)):
    users=db.query(User).all()
    data=[]
    for user in users:
        temp={"username":user.username}
        data_expenses=[]
        for expense in user.expenses:
            data_expenses.append({"category":expense.category,"amount":expense.amount})
        temp["expenses"]=data_expenses
        data.append(temp)
    return data
            
        
@router.get("/users-with-completed-tasks")
def users_with_completed_tasks(db: Session= Depends(get_db)):
    users=db.query(User).all()
    data=[]
    for user in users:
        temp={"username":user.username}
        data_completed_tasks=[]
        for task in user.tasks:
            if task.status=="completed":
                data_completed_tasks.append(task.title)
        temp["completed_tasks"]=data_completed_tasks
        data.append(temp)
    return data
        
@router.get("/users-summary")
def users_summary(db:Session=Depends(get_db)):
    users=db.query(User).all()
    data=[]
    for user in users:
        data.append({"username":user.username,
                    "total_tasks":len(user.tasks),
                    "completed_tasks":sum(1 for task in user.tasks if task.status=="completed"),
                    "total_expenses":sum(expense.amount for expense in user.expenses)})
    return data



@router.delete("/user/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    try:

        user_to_be_deleted = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user_to_be_deleted:
            raise ValueError("User not found")

        db.delete(user_to_be_deleted)

        db.commit()

        return {
            "message": "User deleted successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
        