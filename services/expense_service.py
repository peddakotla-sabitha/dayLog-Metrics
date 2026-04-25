from models.expenses import Expense
from utils.file_handler import read_json,write_json
from config import DATA_FILE
def add_expense(amount,category):
    data=read_json(DATA_FILE)
    try:
        expense_obj = Expense(amount, category)
    except ValueError:
        raise ValueError("Invalid amount. Please enter numeric value")
    expense_dict = expense_obj.to_dict()    
    data["expenses"].append(expense_dict)
    write_json(DATA_FILE,data)
    return expense_dict
    
def get_all_expenses(): #displays all expenses
    data=read_json(DATA_FILE)
    return data["expenses"]


def delete_expense(expense_id): #deletes an expense
    data=read_json(DATA_FILE)
    old_length=len(data["expenses"])
    newExpenses=[expense for expense in data["expenses"] if expense["id"]!=expense_id]
    new_length=len(newExpenses)
    
    if old_length==new_length:
        raise ValueError("Expense not found")
    data["expenses"]=newExpenses
    write_json(DATA_FILE,data)
    return "Expense Deleted Successfully"