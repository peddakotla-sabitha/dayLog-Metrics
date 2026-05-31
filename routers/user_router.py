from fastapi import HTTPException, Depends, APIRouter
from schemas.user_schema import UserCreate,UserDashboard
from database import get_db
from sqlalchemy.orm import Session
from services.user_service import create_user,authenticate_user, get_dashboard
from utils.auth import create_access_token, get_current_user
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
    
    
# Dashboard
@router.get("/dashboard",response_model=UserDashboard, summary="User Dashboard",tags=["Dashboard"])
def user_dashboard(db: Session=Depends(get_db),current_user: User=Depends(get_current_user)):
    try:
        users_summary=get_dashboard(db,current_user.id)
        return users_summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
