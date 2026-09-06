from datetime import datetime

class TransactionModel:
    def __init__(self, id: int, amount: float, type: str, category: str, created_at: datetime, description: str = None):
        self.id = id
        self.amount = amount
        self.type = type  # 'income' or 'expense'
        self.category = category
        self.created_at = created_at
        self.description = description