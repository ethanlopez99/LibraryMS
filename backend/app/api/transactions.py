from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, security
from .database import get_db
from .models import TransactionCreate
from .errors import ErrorMessages

router = APIRouter(prefix="/transactions")

@router.post("/")
def new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise ErrorMessages.NOT_AUTHORIZED

    transaction_data = {'book_id': transaction.book_id, 'lender_id': transaction.lender_id, 'transaction_type': transaction.transaction_type}


    try:
        new_transaction_data = crud.new_transaction(db, transaction_data)
        if (new_transaction_data):
            return new_transaction_data
    except HTTPException as e:
        raise e
    except:
        raise ErrorMessages.UNKNOWN_ERROR_OCCURRED

# Delete all transactions
@router.get("/removeall")
def remove_all_transactions(db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    crud.delete_books(db=db)
    return {"message": "All transactions deleted"}

@router.get("/")
def get_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    return crud.get_transactions(db, skip, limit)