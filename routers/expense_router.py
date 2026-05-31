from fastapi import HTTPException, Depends, APIRouter
from schemas.expense_schema import ExpenseCreate, ExpenseResponse,ExpenseUpdate,ExpenseResponseDetails
from services.expense_service import get_all_expenses,delete_expense,add_expense,expense_update,Expense_details
from models.users import  User
from database import get_db
from sqlalchemy.orm import Session
from utils.auth import get_current_user


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

@router.put("/expenses/{expense_id}",response_model=ExpenseResponse,status_code=200,summary="Updating an expense", tags=["Updating an expense"])
def update_expense(expense_id: str,expense:ExpenseUpdate, db: Session=Depends(get_db),current_user: User=Depends(get_current_user)):
    try:
        updated_details=expense_update(db,expense_id,current_user.id,expense.amount,expense.category,)
        return updated_details
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/expenses/details",response_model=list[ExpenseResponseDetails],summary="expense details",tags=["expense_details"])
def expense_details(db:Session=Depends(get_db),current_user: User=Depends(get_current_user)):
    try:
        details=Expense_details(db,current_user.id)
        return details
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    

        
        

