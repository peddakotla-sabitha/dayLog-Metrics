from fastapi import HTTPException, Depends, APIRouter
from schemas.expense_schema import ExpenseCreate, ExpenseResponse
from services.expense_service import get_all_expenses,delete_expense,add_expense
from models.users import  User
from database import get_db
from sqlalchemy.orm import Session,joinedload
from utils.auth import get_current_user
from models.expenses import Expense


router=APIRouter()


#EXPENSES SERVICES
@router.get("/expenses", summary = "Fetch all expenses", response_model=list[ExpenseResponse],tags=["Fetch all expenses"], status_code=200)
def fetch_expenses(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return get_all_expenses(db, current_user.id)

@router.post("/expenses", summary= "add an expense", tags = ["add an expense"],status_code=201)
def create_expense(expense: ExpenseCreate, db: Session=Depends(get_db),current_user: User=Depends(get_current_user)):
    try:
        return add_expense(db, expense.amount,expense.category, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/expenses/{expense_id}", summary = "Deleting an expense", tags=["Deleting an expense"], status_code=200)
def remove_expense(expense_id: str, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    try:
        delete_expense(db, expense_id,current_user.id)
        return {"message": "Expense Deleted Successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

        
        

