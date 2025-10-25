from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.db.database import base

class Transaction(base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    from_currency = Column(String, nullable=False)
    to_currency = Column(String, nullable=False)
    from_value = Column(Float, nullable=False)
    to_value = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)