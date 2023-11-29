
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, security
from .database import get_db
from .models import AdminCreate, Token
from .validation import validate_username, validate_password

router = APIRouter(prefix="/admins")

# Get all admins from the database
@router.get("/")
def get_all_admins(db: Session = Depends(get_db)):
    admins = crud.get_all_admins(db)
    return admins

@router.get("/{admin_id}")
def get_admin_by_id(admin_id: int, db: Session = Depends(get_db)):
    admin = crud.get_admin(db, admin_id)
    return admin


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
    
    try:
        validate_username(admin_data.username)
        validate_password(admin_data.password)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))

    admin_data = {'username': admin_data.username, 'password': admin_data.password}

    try:
        admin = crud.create_admin(db, admin_data)
        return admin
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) # 409 used for Conflict
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Update an existing admin
@router.post("/update")
def update_admin(new_admin_data: dict, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")
    # admin id extracted from token
    try:
        validate_password(new_admin_data['password'])
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    
    db_admin = crud.update_admin(admin_id=token['id'], update_data=new_admin_data, db=db)
    if db_admin:
        return db_admin
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update admin")
