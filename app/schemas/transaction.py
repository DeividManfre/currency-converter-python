from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    name: str
    user_id: int
    from_currency: str
    to_currency: str
    value: float

class TransactionResponse(BaseModel):
    id: int
    name: str
    user_id: int
    from_currency: str
    to_currency: str
    from_value: float
    to_value: float
    rate: float
    timestamp: datetime

    class Config:
        from_attributes = True
