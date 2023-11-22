from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from api import crud, security
from .database import get_db
from .models import Book, BookCreate, Token

router = APIRouter(prefix="/books")

@router.get("/")
def get_all_books(db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    books = crud.get_all_books(db)
    return books

@router.get("/search")
def search_by_name(title: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    books = crud.search_books_by_name(db, title, skip=skip, limit=limit)
    return books

@router.post("/new")
def create_new_book(book_data: BookCreate, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    new_book_data = {'title': book_data.title, 'author': book_data.author}
    book = crud.new_book(db=db, book_data=new_book_data)
    if book:
        return book
    else:
        raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add new book")

@router.post("/update")
def update_book(book_id: int, new_book_data: dict, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    db_book = crud.update_book(book_id=book_id, update_data=new_book_data, db=db)
    if db_book:
        return db_book
    else:
        raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update book")
        
