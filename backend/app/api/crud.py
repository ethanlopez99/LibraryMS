from sqlalchemy.orm import Session
from .models import Admin, AdminCreate, Book, BookCreate, Lender, LenderCreate, Transaction, TransactionCreate

from passlib.context import CryptContext


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

def new_transaction(db: Session, transaction_data: TransactionCreate):
    db_transaction = Transaction(book_id=transaction_data['book_id'], lender_id=transaction_data['lender_id'], transaction_type=transaction_data['transaction_type'])
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Added pagination functionality
def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()