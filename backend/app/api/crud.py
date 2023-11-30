from sqlalchemy.orm import Session
from .models import Admin, AdminCreate, Book, BookCreate, Lender, LenderCreate, Transaction, TransactionCreate
from .errors import ErrorMessages
from sqlalchemy import func, or_, and_

from passlib.context import CryptContext

# ===== ADMIN CRUD FUNCTIONS ===== #

def create_admin(db: Session, admin_data: AdminCreate):
    # Check if the username already exists
    existing_admin = db.query(Admin).filter(Admin.username == admin_data['username']).first()

    if existing_admin:
        # Raise an exception or return a specific value to indicate the failure
        raise ErrorMessages.ALREADY_EXISTING_ADMIN
    # New admin data created as Admin object. Uses "hash_password" to hash the password and store it encrypted in the db
    db_admin = Admin(username=admin_data['username'], password=hash_password(admin_data['password']))
    # Object added to DB
    db.add(db_admin)
    # Changes commited to DB
    db.commit()
    # DB refreshed to verify changes
    db.refresh(db_admin)
    # Return new admin data
    return db_admin


def get_all_admins(db: Session):
    # get all rows from Admin table
    return db.query(Admin).all()

def count_admins(db: Session):
    # count number of rows in Admin table
    return db.query(Admin).count()

def get_admin(db:Session, admin_id: int):
    # get admin row by admin id
    return db.query(Admin).filter(Admin.id == admin_id).first()

def update_admin(db: Session, admin_id: int, update_data: dict):
    # Verify admin exists before trying to update
    db_admin = get_admin(db, admin_id)
    # If admin exists, iterate through fields to change
    if db_admin:
        for key, value in update_data.items():
            # If keys include password, make sure to hash password before adding to DB
            if key == 'password':
                setattr(db_admin, key, hash_password(value))
            else:
                setattr(db_admin, key, value)
        # Commit changes to DB
        db.commit()
        # Refresh DB to verify changes
        db.refresh(db_admin)
        # Return new admin data
        return db_admin
    # If admin not found, return None
    return None

def delete_admins(db: Session):
    db.query(Admin).delete()
    db.commit()


# Create password context
pw_context = CryptContext(schemes=["bcrypt"])

# Hash password given a password string and return it
def hash_password(password:str):
    return pw_context.hash(password)

# ===== TRANSACTION CRUD FUNCTIONS ===== #

# new transaction method, used for loans and returns
def new_transaction(db: Session, transaction_data: TransactionCreate):
    # transaction data obtained from inputs
    db_transaction = Transaction(book_id=transaction_data['book_id'], lender_id=transaction_data['lender_id'], transaction_type=transaction_data['transaction_type'])

    # check if book is available, to find out if transaction type requested is possible
    available = is_book_available(db, db_transaction.book_id)
    if (available == False and db_transaction.transaction_type == 1):
        return None # Cannot loan a book if not available
    elif (available == True and db_transaction.transaction_type == 0):
        return None # Cannot return a book if it has not been loaned
    
    # Find book to update is_available
    book = db.query(Book).filter(Book.id == transaction_data['book_id'])
    # Find lender id of book, if exists
    book_lender_id = db.query(Book.lender_id).filter(Book.id == transaction_data['book_id']).all()[0].lender_id

    # If returning, and input lender_id does not match lender_id in database, return none
    if (db_transaction.transaction_type == 0 and not book_lender_id == db_transaction.lender_id):
        return None # Lender ID must match to be able to return book
    
    # Add new transaction to database, and commit changes and refresh
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    # Update book row to change status accordingly, based on transaction type
    book.update({'is_available': (False if db_transaction.transaction_type == 1 else True), 'lender_id': db_transaction.lender_id})
    db.commit()
    db.refresh(db_transaction)
    # return db transaction
    return db_transaction


# Added pagination functionality
def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()

# Drop Transactions table
def delete_transactions(db: Session):
    db.query(Book).update({"is_available": True})
    db.commit()
    db.refresh()
    db.query(Transaction).delete()
    db.commit()
    db.refresh()

# ===== BOOKS CRUD FUNCTIONS ===== #

def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    # Get all books from Book table
    return db.query(Book).offset(skip).limit(limit).all()

def search_books_by_name(db: Session, book_name: str, skip: int = 0, limit: int = 10):
    # Search books based off title
    return db.query(Book).filter(or_(Book.title.ilike(book_name),(Book.author.ilike(book_name)))).offset(skip).limit(limit).all()



def new_book(db: Session, book_data: BookCreate):
    # New book data stored as Book object
    new_book_data = Book(title=book_data['title'], author=book_data['author'])
    # Add new book data, commit and refresh
    db.add(new_book_data)
    db.commit()
    db.refresh(new_book_data)
    # Return new book data, including new ID
    return new_book_data

def is_book_available(db: Session, book_id: int):
    # returns book availability based on is_available column on database
    result = db.query(Book.is_available).filter(Book.id == book_id).first()
    return result.is_available if result else None

def update_book(db: Session, update_data: dict):
    # Find book to update based on input book_id
    db_book = db.query(Book).filter(Book.id == update_data['id']).first()
    # if book exists, iterate through each item in update_data
    if db_book:
        for key, value in update_data.items():
            # update attributes for each key based on value
            setattr(db_book, key, value)
        # commit changes to db and refresh
        db.commit()
        db.refresh(db_book)
        #return new book data
        return db_book
    #if book not found, return none
    return None

def count_books(db: Session):
    # returns count of all rows in Book
    return db.query(Book).count()

def count_books_by_name(title: str, db: Session, unavailable: bool = False):
    # returns count of all rows in Book matching the input
    if not unavailable:
        return db.query(Book).filter(or_(Book.title.ilike(title),(Book.author.ilike(title)))).count()
    else:
        return db.query(Book).filter(and_((Book.is_available == False),or_(Book.title.ilike(title),(Book.author.ilike(title))))).count()

def get_all_unavailable_books_by_name(db: Session, title: str, skip: int = 0, limit: int = 10):
    # Returns books based off availability
    return db.query(Book).filter(and_(Book.is_available == False),(Book.title.ilike(title))).offset(skip).limit(limit).all()

def count_unavailable_books(db: Session):
    # Counts unavailable books
    return db.query(Book).filter(Book.is_available == False).count()

def get_most_lent_books(db: Session, limit: int = 5):
    # Gets top 5 (unless passed different) books, returning book object based off times it's been loaned out
    return (
        # counts how many times a book ID occurs in transaction column
        db.query(Book, func.count(Transaction.book_id).label("count"))
        # joins transaction and book tables, based on book id
        .join(Transaction, Transaction.book_id == Book.id)
        # filters to only loans
        .filter(Transaction.transaction_type == 1)
        .group_by(Book)
        # Orders in descending fashion to get top 5
        .order_by(func.count(Transaction.book_id).desc())
        .limit(limit)
        .all()
    )

# Drop Books table
def delete_books(db: Session):
    db.query(Book).delete()
    db.commit()
    db.refresh()


# ===== LENDERS CRUD FUNCTIONS ===== #

def get_all_lenders(db: Session, skip: int = 0, limit: int = 10):
    # Get all lenders
    return db.query(Lender).offset(skip).limit(limit).all()

def search_lender_by_name(db: Session, lender_name: str, skip: int = 0, limit: int = 10):
    # Get all lenders based by name
    return db.query(Lender).filter(Lender.lender_name.ilike(lender_name)).offset(skip).limit(limit).all()

def count_lenders(db: Session):
    # Counts rows in Lender table
    return db.query(Lender).count()

def new_lender(db: Session, lender_data: LenderCreate):
    # new lender data is stored as Lender object
    new_lender_data = Lender(lender_name=lender_data['lender_name'])
    # new data is added to database and committed
    db.add(new_lender_data)
    db.commit()
    db.refresh(new_lender_data)
    # return new lender data, including id
    return new_lender_data

def update_lender(db: Session, update_data: dict):
    # finds lender based on lender id
    db_lender = db.query(Lender).filter(Lender.id == update_data['id']).first()
    if db_lender:
        # if lender exists, update based on update_data
        for key, value in update_data.items():
            if key == "id":
                next
            setattr(db_lender, key, value)
        # commit and refresh
        db.commit()
        db.refresh(db_lender)
        # return updated lender
        return db_lender
    # if lender not found, return None
    return None

# Drop Lenders table
def delete_lenders(db: Session):
    db.query(Lender).delete()
    db.commit()
    db.refresh()