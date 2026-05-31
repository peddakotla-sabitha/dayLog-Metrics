from sqlalchemy.orm import Session,joinedload
from sqlalchemy import or_
from models.users import User
from utils.security import hash_password,verify_password

def create_user(db: Session, username: str, email: str, password: str):
    existing_user=db.query(User).filter(
        or_(User.email==email, User.username==username)
        ).first()
    if existing_user:
        if existing_user.email==email:
            raise ValueError("Email already exists")
        if existing_user.username==username:
            raise ValueError("username already exists")
        
    new_user=User(username=username,email=email, hashed_password=hash_password(password))
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return "Registration Successful"
    except Exception as e:
        db.rollback()
        raise ValueError("User creation failed")
def authenticate_user(db: Session, email: str, password: str):
    existing_user=db.query(User).filter(User.email==email).first()
    if not existing_user:
        raise ValueError("Invalid Credentials")
    if not verify_password(password,existing_user.hashed_password):
        raise ValueError("Invalid Credentials")
    return existing_user


def get_dashboard(db: Session,user_id: str):
    user=db.query(User).filter(User.id==user_id).options(joinedload(User.tasks),joinedload(User.expenses)).first()
    if not user:
        raise ValueError("user not found")
    total_tasks=len(user.tasks)
    completed_tasks=sum(1 for task in user.tasks if task.status=="completed")
    return {"total_tasks":total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks":total_tasks-completed_tasks,
            "total_expenses":sum(expense.amount for expense in user.expenses)}