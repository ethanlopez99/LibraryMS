
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from api import crud, security
from .database import get_db
from .models import Lender, LenderCreate, Token

router = APIRouter(prefix="/lenders")

# Get all lenders
@router.get("/")
def get_all_lenders(db: Session = Depends(get_db), skip: int = 0, limit: int = 10, token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    lenders = crud.get_all_lenders(db=db, skip=skip, limit=limit)
    return lenders

# Count all lenders
@router.get("/count/all")
def count_lenders(db: Session = Depends(get_db)):
    count = crud.count_lenders(db)
    return count

# Search lenders by name
@router.get("/search")
def search_by_name(lender_name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    lenders = crud.search_lender_by_name(db, lender_name, skip=skip, limit=limit)
    return lenders

# Create a new lender
@router.post("/new")
def create_new_lender(lender_data: LenderCreate, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    new_lender_data = {'lender_name': lender_data.lender_name}
    lender = crud.new_lender(db=db, lender_data=new_lender_data)
    if lender:
        return lender
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add new lender")

# Update a lender
@router.post("/update")
def update_lender(lender_id: int, new_lender_data: dict, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    db_lender = crud.update_lender(lender_id=lender_id, update_data=new_lender_data, db=db)
    if db_lender:
        return db_lender
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update lender")
