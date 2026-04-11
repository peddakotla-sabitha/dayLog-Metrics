import uuid
from datetime import datetime
class Expense:
    def __init__(self,amount,category):
        self.id=str(uuid.uuid4())
        self.amount=float(amount)
        self.category=category
        self.date=datetime.now().strftime("%Y-%m-%d")
        
    def to_dict(self):
        return {"id":self.id, "amount":self.amount, "category":self.category, "date":self.date}