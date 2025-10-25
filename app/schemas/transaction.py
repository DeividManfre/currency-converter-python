from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    user_id: int
    from_currency: str
    to_currency: str
    value: float

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    from_currency: str
    to_currency: str
    from_value: float
    to_value: float
    rate: float
    timestamp: datetime

    class Config:
        orm_mode = True
