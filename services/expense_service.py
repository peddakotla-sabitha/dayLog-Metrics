from models.expenses import Expense
from utils.file_handler import read_json,write_json
from config import DATA_FILE
from sqlalchemy.orm import Session,joinedload

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


def expense_update(
    db: Session,
    expense_id: str,
    user_id: str,
    amount: float | None = None,
    category: str | None = None
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()

    if not expense:
        raise ValueError("Expense not found")

    if amount is None and category is None:
        raise ValueError("Enter details for updation")

    no_amount_change = (
        amount is None or amount == expense.amount
    )

    no_category_change = (
        category is None or category == expense.category
    )

    if no_amount_change and no_category_change:
        raise ValueError("No changes detected")

    if amount is not None:
        expense.amount = amount

    if category is not None:
        expense.category = category

    db.commit()
    db.refresh(expense)

    return expense



def Expense_details(db: Session,user_id: str):
    expense=db.query(Expense).filter(Expense.user_id==user_id).options(joinedload(Expense.user)).all()
    if not expense:
        raise ValueError("Expenses not found")
    return expense