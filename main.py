from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from datetime import datetime
from schemas import TransactionCreate, TransactionResponse

app = FastAPI(title="Personal Budget & Expense Management System")

# Временное хранилище в памяти вместо PostgreSQL (пока не подключили БД)
fake_db_transactions = []
counter_id = 1


@app.post("/transactions/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate):
    global counter_id
    new_tx = {
        "id": counter_id,
        "amount": transaction.amount,
        "type": transaction.type,
        "category": transaction.category,
        "description": transaction.description,
        "created_at": datetime.now()
    }
    fake_db_transactions.append(new_tx)
    counter_id += 1
    return new_tx


@app.get("/transactions/", response_model=List[TransactionResponse])
def get_transactions(type: Optional[str] = None):
    if type:
        return [tx for tx in fake_db_transactions if tx["type"] == type]
    return fake_db_transactions


@app.get("/budget/summary")
def get_budget_summary():
    total_income = sum(tx["amount"] for tx in fake_db_transactions if tx["type"] == "income")
    total_expense = sum(tx["amount"] for tx in fake_db_transactions if tx["type"] == "expense")
    balance = total_income - total_expense

    return {
        "balance": balance,
        "total_income": total_income,
        "total_expense": total_expense
    }