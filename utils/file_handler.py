import json
def read_json(file_name):
    try:
        with open(file_name,"r") as file:
            return json.load(file) 
    except:
        return {"tasks": [], "expenses": []}
def write_json(file_name,data):
    with open(file_name,"w") as file:
        json.dump(data,file)
        

#read_json(r"C:\Users\dimpu\Desktop\Project_task_and_expenses\data\data.json")

#write_json(r"C:\Users\dimpu\Desktop\Project_task_and_expenses\data\data.json")