from fastapi import FastAPI
from app.api.routes_transactions import router as transaction_router
from app.db.database import base, engine

base.metadata.create_all(bind=engine)

app = FastAPI(title="Currency Converter API", version="1.0")

app.include_router(transaction_router)