from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import session_local as SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.currency_service import get_conversion_rate
from app.auth.utils import AuthUtils

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db),
                             current_user: str = Depends(AuthUtils.get_current_user)):
    rate = await get_conversion_rate(transaction.from_currency, transaction.to_currency)
    to_value = transaction.value * rate

    db_transaction = Transaction(
        name=f"{transaction.from_currency}_to_{transaction.to_currency}",
        user_id=transaction.user_id,
        from_currency=transaction.from_currency,
        to_currency=transaction.to_currency,
        from_value=transaction.value,
        to_value=to_value,
        rate=rate,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=list[TransactionResponse])
def get_transactions(userId: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == userId).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user")
    return transactions

@router.get("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.delete("/{transaction_id}", response_model=dict)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}