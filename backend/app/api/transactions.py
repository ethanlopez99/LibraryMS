from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import crud, security
from .database import SessionLocal
from .models import Transaction, TransactionCreate, Token

router = APIRouter(prefix="/transactions")

# Used to create new sessions of database for each request, to manage lifecycle of db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    return crud.create_transaction(db, transaction)

@router.get("/")
def get_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    return crud.get_transactions(db, skip, limit)