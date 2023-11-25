
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import crud, security, models
from .database import get_db
from .models import Admin, AdminCreate, Token

router = APIRouter(prefix="/admins")

# Get all admins from the database
@router.get("/")
def get_all_admins(db: Session = Depends(get_db)):
    admins = crud.get_all_admins(db)
    return admins

# Validate admin credentials and return a token
@router.post("/login", response_model=Token)
def validate_credentials(admin_data: AdminCreate, db: Session = Depends(get_db)):
    return (security.login(db, admin_data))

# Count the number of admins in the database
@router.get("/count/all")
def count_admins(db: Session = Depends(get_db)):
    count = crud.count_admins(db)
    return count

# Register a new admin
@router.post("/register")
def register_admin(admin_data: AdminCreate, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")

    admin_data = {'username': admin_data.username, 'password': admin_data.password}
    admin = crud.create_admin(db, admin_data)
    if admin:
        return admin
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create admin")

# Update an existing admin
@router.post("/update")
def update_admin(admin_id: int, new_admin_data: dict, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    db_admin = crud.update_admin(admin_id=admin_id, update_data=new_admin_data, db=db)
    if db_admin:
        return db_admin
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update admin")
