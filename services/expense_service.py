from models import expenses
from utils.file_handler import read_json,write_json
DATA_FILE=r"C:\Users\dimpu\Desktop\Project_task_and_expenses\data\data.json"
def add_expense(amount,category):
    data=read_json(DATA_FILE)
    try:
        expense_obj=expenses.Expense(amount,category)
        expense_dict=expense_obj.to_dict()
    except ValueError:
        return "Invalid amount. Please enter numeric value"
    data["expenses"].append(expense_dict)
    write_json(DATA_FILE,data)
    return "Expense added successfully"
    
def get_all_expenses(): #displays all expenses
    data=read_json(DATA_FILE)
    return data["expenses"]


def delete_expense(expense_id): #deletes an expense
    data=read_json(DATA_FILE)
    old_length=len(data["expenses"])
    newExpenses=[expense for expense in data["expenses"] if expense["id"]!=expense_id]
    new_length=len(newExpenses)
    
    if old_length==new_length:
        return "Expense not found"
    data["expenses"]=newExpenses
    write_json(DATA_FILE,data)
    return "Expense deleted successfully"
    
            