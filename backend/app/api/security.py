from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException



from .models import Admin, AdminCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pw_context = CryptContext(schemes=["bcrypt"])
secret_token = "secret"



def login(db: Session, admin_data: AdminCreate):
    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if admin and pw_context.verify(admin_data.password, admin.password):
        return {"access_token": create_jwt_token(data={"sub": admin.username}), "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_jwt_token(data: dict):
    return jwt.encode(data, "secret_token", algorithm="HS256")

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not authenticate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, "secret_token", algorithms=["HS256"])
        return payload
    except JWTError:
        raise credentials_exception