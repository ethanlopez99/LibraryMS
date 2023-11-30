
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import crud, security
from .database import get_db
from .errors import ErrorMessages
from .models import Book, BookCreate, Token
from .validation import validate_author, validate_genre, validate_title

router = APIRouter(prefix="/books")

# Get all books from the database
@router.get("/")
def get_all_books(db: Session = Depends(get_db), token: dict = Depends(security.verify_token), skip: int = 0):
    if "sub" not in token:
        raise ErrorMessages.NOT_AUTHORIZED
    books = crud.get_all_books(db=db, skip=skip)
    return books

@router.get("/search/unavailable")
def get_all_unavailable_books(title: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise ErrorMessages.NOT_AUTHORIZED
    books = crud.get_all_unavailable_books_by_name(db = db, title = title, limit = limit, skip = skip)
    return books

# Delete all books
@router.get("/removeall")
def remove_all_books(db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise ErrorMessages.NOT_AUTHORIZED
    crud.delete_books(db=db)
    return {"message": "All books deleted"}

# Search books by name
@router.get("/search")
def search_by_name(title: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise ErrorMessages.NOT_AUTHORIZED
    books = crud.search_books_by_name(db, title, skip=skip, limit=limit)
    return books

# Count all books in the database
@router.get("/count/all")
def count_books(db: Session = Depends(get_db)):
    count = crud.count_books(db)
    return count

# Count all unavailable books in the database
@router.get("/count/unavailable")
def count_unavailable_books(db: Session = Depends(get_db)):
    count = crud.count_unavailable_books(db)
    return count

# Get popular books from the database
@router.get("/popular")
def get_popular_books(db: Session = Depends(get_db), limit: int = 10):
    popular_books = crud.get_most_lent_books(db, limit)
    return popular_books

# Create a new book in the database
@router.post("/new")
def create_new_book(book_data: BookCreate, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise ErrorMessages.NOT_AUTHORIZED
    
    try:
        validate_title(book_data.title)
        validate_author(book_data.author)
        validate_genre(book_data.genre)
    except HTTPException as e:
        raise e

    new_book_data = {'title': book_data.title, 'author': book_data.author, 'genre': book_data.genre}
    book = crud.new_book(db=db, book_data=new_book_data)
    if book:
        return book
    else:
        raise ErrorMessages.UNKNOWN_ERROR_OCCURRED

# Update a book in the database. As it's already existing book, BookCreate cannot be used
@router.post("/update")
def update_book(new_book_data: dict, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise ErrorMessages.NOT_AUTHORIZED
    
    if "id" not in new_book_data:
        raise ErrorMessages.BOOK_ID_MISSING
    
    try:
        validate_title(new_book_data['title'])
    except HTTPException as e:
        raise e
    except KeyError:
        raise ErrorMessages.TITLE_MISSING
    
    try:
        validate_author(new_book_data['author'])
    except HTTPException as e:
        raise e
    except KeyError:
        raise ErrorMessages.AUTHOR_MISSING

    try:
        validate_genre(new_book_data['genre'])
    except HTTPException as e:
        raise e
    except KeyError:
        raise ErrorMessages.GENRE_MISSING
    
    new_book_data = {"id": new_book_data['id'], "title":new_book_data['title'], "author":new_book_data['author']}
    
    db_book = crud.update_book(update_data=new_book_data, db=db)
    if db_book:
        return db_book
    else:
        raise ErrorMessages.UNKNOWN_ERROR_OCCURRED
