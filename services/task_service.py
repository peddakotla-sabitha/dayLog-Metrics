from utils.file_handler import read_json, write_json
from config import DATA_FILE
from models.task import Task
def add_task(title):
    #reading the existing data
    data=read_json(DATA_FILE) #data is a dictionary
    
    #creating an object to task class
    newTask=Task(title)
    
    # converting to a dictionary
    taskDict=newTask.to_dict() 
    #adding new task to the list
    data["tasks"].append(taskDict)
    
    #writing all data to jsonfile
    write_json(DATA_FILE,data)
    
    return taskDict
def get_all_tasks():
    data=read_json(DATA_FILE)
    return data["tasks"]
def delete_task(task_id):
    data=read_json(DATA_FILE)
    old_length=len(data["tasks"])
    newTasks=[task for task in data["tasks"] if task["id"]!=task_id]
    new_length=len(newTasks)
    if old_length==new_length:
        raise ValueError("Task not found")
    data["tasks"]=newTasks
    write_json(DATA_FILE,data)
    return "Task deleted successfully"
def update_task_status(task_id):
    data=read_json(DATA_FILE)
    for task in data["tasks"]:
        if task["id"]==task_id:
            task["status"]="completed"
            write_json(DATA_FILE, data)
            return task
    
    raise ValueError("Task not found")
    
    
    