from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import session_local
from app.auth.models_user import User
from app.auth.utils import AuthUtils
from app.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if not AuthUtils.is_password_strong(data.password):
        suggestion = AuthUtils.suggest_password()
        raise HTTPException(status_code=400, detail=f"Password does not meet strength requirements. Suggested password: {suggestion}")

    hashed_pw = AuthUtils.hashed_password(data.password)
    user = User(name=data.name, email=data.email, password_hash=hashed_pw)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not AuthUtils.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = AuthUtils.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
