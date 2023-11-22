from sqlalchemy.orm import Session
from .models import Admin, AdminCreate, Book, BookCreate, Lender, LenderCreate, Transaction, TransactionCreate

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

def get_admin(db:Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()

def updateAdmin(db: Session, admin_id: int, update_data: dict):
    db_admin = get_admin(db, admin_id)
    if db_admin:
        for key, value in update_data.items():
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
    if (not is_book_available(db, db_transaction.book_id) and db_transaction.transaction_type == 1):
        return None # Cannot loan a book if not available
    elif (is_book_available(db, db_transaction.book_id) and db_transaction.transaction_type == 0):
        return None # Cannot return a book if it has not been loaned
    
    db.add(db_transaction)
    db.commit()

    # Update book row to change status
    db.query(Book).filter(Book.id == transaction_data['book_id']).update({'is_available': (False if db_transaction.transaction_type == 1 else True), 'lender_id': db_transaction.lender_id})
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
    return db.query(Book).filter(Book.title.ilike(f"%{book_name}")).offset(skip).limit(limit).all()

def new_book(db: Session, book_data: BookCreate):
    new_book_data = Book(title=book_data['title'], author=book_data['author'])
    db.add(new_book_data)
    db.commit()
    db.refresh(new_book_data)
    return new_book_data

def is_book_available(db: Session, book_id: str):
    return db.query(Book.is_available).filter(Book.id == book_id)


# ===== LENDERS CRUD FUNCTIONS ===== #

def get_all_lenders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Lender).offset(skip).limit(limit).all()

def search_lender_by_name(db: Session, lender_name: str, skip: int = 0, limit: int = 10):
    return db.query(Lender).filter(Lender.name.ilike(f"%{lender_name}")).offset(skip).limit(limit).all()

def new_lender(db: Session, lender_data: Lender):
    new_lender_data = Lender(lender_name=lender_data['lender_name'])
    db.add(new_lender_data)
    db.commit()
    db.refresh(new_lender_data)
    return new_lender_data