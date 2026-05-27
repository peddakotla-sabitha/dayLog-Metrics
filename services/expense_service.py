from models.expenses import Expense
from utils.file_handler import read_json,write_json
from config import DATA_FILE
from sqlalchemy.orm import Session

#ADD AN EXPENSE
def add_expense(db:Session, amount: float,category: str,user_id:str):
    
    new_expense=Expense(amount=amount, category=category,user_id=user_id)
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense
    
    
#GET ALL EXPENSES
def get_all_expenses(db: Session, user_id: str): #displays all expenses
    return db.query(Expense).filter(user_id==Expense.user_id).all()


#DELETE AN EXPENSE
def delete_expense(db: Session,expense_id: str, user_id: str): #deletes an expense
   expense=db.query(Expense).filter(Expense.id==expense_id, Expense.user_id==user_id).first()
   if not expense:
       raise ValueError(f"Expense with id {expense_id} is not found or not authorized")
   db.delete(expense)
   db.commit()
   return True