from sqlalchemy.orm import Session
from .models import Admin, AdminCreate, Book, BookCreate, Lender, LenderCreate, Transaction, TransactionCreate

from sqlalchemy import func

from passlib.context import CryptContext

# ===== ADMIN CRUD FUNCTIONS ===== #

def create_admin(db: Session, admin_data: AdminCreate):
    db_admin = Admin(username=admin_data['username'], password=hash_password(admin_data['password']))
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_all_admins(db: Session):
    return db.query(Admin).all()

def count_admins(db: Session):
    return db.query(Admin).count()

def get_admin(db:Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()

def update_admin(db: Session, admin_id: int, update_data: dict):
    db_admin = get_admin(db, admin_id)
    if db_admin:
        for key, value in update_data.items():
            if key == 'password':
                setattr(db_admin, key, hash_password(value))
            else:
                setattr(db_admin, key, value)
        db.commit()
        db.refresh(db_admin)
        return db_admin
    return None

pw_context = CryptContext(schemes=["bcrypt"])

def hash_password(password:str):
    return pw_context.hash(password)

# ===== TRANSACTION CRUD FUNCTIONS ===== #

def new_transaction(db: Session, transaction_data: TransactionCreate):
    db_transaction = Transaction(book_id=transaction_data['book_id'], lender_id=transaction_data['lender_id'], transaction_type=transaction_data['transaction_type'])

    available = is_book_available(db, db_transaction.book_id)
    if (available == False and db_transaction.transaction_type == 1):
        return None # Cannot loan a book if not available
    elif (available == True and db_transaction.transaction_type == 0):
        return None # Cannot return a book if it has not been loaned
    
    book = db.query(Book).filter(Book.id == transaction_data['book_id'])
    book_lender_id = db.query(Book.lender_id).filter(Book.id == transaction_data['book_id']).all()[0].lender_id

    if (db_transaction.transaction_type == 0 and not book_lender_id == db_transaction.lender_id):
        return None # Lender ID must match to be able to return book
    
    db.add(db_transaction)
    db.commit()

    # Update book row to change status
    book.update({'is_available': (False if db_transaction.transaction_type == 1 else True), 'lender_id': db_transaction.lender_id})
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# Added pagination functionality
def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()

# ===== BOOKS CRUD FUNCTIONS ===== #

def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def search_books_by_name(db: Session, book_name: str, skip: int = 0, limit: int = 10):
    return db.query(Book).filter(Book.title.ilike(book_name)).offset(skip).limit(limit).all()

def new_book(db: Session, book_data: BookCreate):
    new_book_data = Book(title=book_data['title'], author=book_data['author'])
    db.add(new_book_data)
    db.commit()
    db.refresh(new_book_data)
    return new_book_data

def is_book_available(db: Session, book_id: int):
    result = db.query(Book.is_available).filter(Book.id == book_id).all()
    return result[0].is_available if result else None

def update_book(db: Session, update_data: dict):
    db_book = db.query(Book).filter(Book.id == update_data['id']).first()
    if db_book:
        for key, value in update_data.items():
            if key == "book_id":
                next
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

def count_books(db: Session):
    return db.query(Book).count()

def get_all_unavailable_books_by_name(db: Session, title: str, skip: int = 0, limit: int = 10):
    return db.query(Book).filter(Book.title.ilike(title)).filter(Book.is_available == False).filter(Book.title.ilike(title)).offset(skip).limit(limit).all()

def count_unavailable_books(db: Session):
    return db.query(Book).filter(Book.is_available == False).count()

def get_most_lent_books(db: Session, limit: int = 5):
    return (
        db.query(Transaction.book_id, func.count(Transaction.book_id).label("count"))
        .filter(Transaction.transaction_type == 1)
        .group_by(Transaction.book_id)
        .order_by(func.count(Transaction.book_id).desc())
        .limit(limit)
        .all()
    )

# ===== LENDERS CRUD FUNCTIONS ===== #

def get_all_lenders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Lender).offset(skip).limit(limit).all()

def search_lender_by_name(db: Session, lender_name: str, skip: int = 0, limit: int = 10):
    return db.query(Lender).filter(Lender.lender_name.ilike(lender_name)).offset(skip).limit(limit).all()

def count_lenders(db: Session):
    return db.query(Lender).count()

def new_lender(db: Session, lender_data: LenderCreate):
    new_lender_data = Lender(lender_name=lender_data['lender_name'])
    db.add(new_lender_data)
    db.commit()
    db.refresh(new_lender_data)
    return new_lender_data

def update_lender(db: Session, lender_id: int, update_data: dict):
    db_lender = db.query(Lender).filter(Lender.id == lender_id).first()
    if db_lender:
        for key, value in update_data.items():
            setattr(db_lender, key, value)
        db.commit()
        db.refresh(db_lender)
        return db_lender
    return None