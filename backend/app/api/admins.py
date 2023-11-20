from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import crud, security, models
from .database import SessionLocal
from .models import Admin, AdminCreate, Token
from .security import login

router = APIRouter(prefix="/admins")

# Used to create new sessions of database for each request, to manage lifecycle of db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_admins(db: Session = Depends(get_db)):
    admins = crud.get_all_admins(db)
    return admins

@router.post("/login", response_model=Token)
def validate_credentials(admin_data: AdminCreate, db: Session = Depends(get_db)):
    return (login(db, admin_data))

# takes requests in the form of {"username": "my_username", "password":"my_password"}
@router.post("/register")
def register_admin(admin_data: AdminCreate, db: Session = Depends(get_db), token: dict = Depends(security.verify_token)):
    print(token)
    if "sub" not in token:
        raise HTTPException(status_code=401, detail="Not Authorized")

    admin_data = {'username': admin_data.username, 'password': admin_data.password}
    admin = crud.create_admin(db, admin_data)
    if admin:
        return admin
    else:
        raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create admin")