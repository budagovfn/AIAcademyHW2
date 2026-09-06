from pydantic import BaseModel, Field, ConfigDict # Добавь ConfigDict сюда
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")
    type: str = Field(..., description="Transaction type: income or expense")
    category: str = Field(..., min_length=2, description="Category of the transaction")
    description: Optional[str] = None

class TransactionResponse(TransactionCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    # if the obtained entry is not a JSON, but python object.