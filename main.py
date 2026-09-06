from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import engine, Base, get_db
from models import TransactionModel
from schemas import TransactionCreate, TransactionResponse
from fastapi.responses import RedirectResponse



Base.metadata.create_all(bind=engine)



app = FastAPI(title="Personal Budget & Expense Management System")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/transactions/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = TransactionModel(
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        description=transaction.description,
        created_at=datetime.utcnow()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions/", response_model=List[TransactionResponse])
def get_transactions(
    type: Optional[str] = Query(None, description="Filter by type: income or expense"),
    start_date: Optional[datetime] = Query(None, description="Start date filter (YYYY-MM-DDTHH:MM:SS)"),
    end_date: Optional[datetime] = Query(None, description="End date filter (YYYY-MM-DDTHH:MM:SS)"),
    db: Session = Depends(get_db)
):
    query = db.query(TransactionModel)

    if type:
        query = query.filter(TransactionModel.type == type)
    if start_date:
        query = query.filter(TransactionModel.created_at >= start_date)
    if end_date:
        query = query.filter(TransactionModel.created_at <= end_date)

    return query.all()


@app.get("/budget/summary")
def get_budget_summary(db: Session = Depends(get_db)):
    transactions = db.query(TransactionModel).all()

    total_income = sum(tx.amount for tx in transactions if tx.type == "income")
    total_expense = sum(tx.amount for tx in transactions if tx.type == "expense")
    balance = total_income - total_expense

    return {
        "balance": balance,
        "total_income": total_income,
        "total_expense": total_expense
    }