from sqlalchemy.orm import Session
from .models import Admin, Book, Lender

from passlib.context import CryptContext


def create_admin(db: Session, admin_data):
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