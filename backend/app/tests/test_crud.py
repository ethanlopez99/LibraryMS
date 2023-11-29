import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from ..main import app
from ..api.database import Base, get_db


# Database stored in memory, to not impact current db
DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

# Create similar function to get_db, but we use this one for local testing
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

test_token = ""

def test_login(username = "root", password="root"):
    global test_token
    response = client.post(
        "/admins/login",
        json={"username":f"{username}", "password": f"{password}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    test_token = data["access_token"]
    

def test_create_admin():
    response = client.post(
        "/admins/register",
        json={"username": "testuser1", "password": "testpassword1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testuser1"
    assert "id" in data
    admin_id = data["id"]
    
    response = client.get(f"/admins/{admin_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == admin_id
    test_login(username="testuser1",password="testpassword1") # For updating password test

def test_create_duplicate_admin():
    response = client.post(
        "/admins/register",
        json={"username": "testuser1", "password": "testpassword2"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 409, response.text

def test_create_admin_with_empty_password():
    response = client.post(
        "/admins/register",
        json={"username": "testuser1", "password": ""},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 400, response.text


def test_create_new_book():
    book_data = {"title": "Test Book", "author": "Test Author"}
    response = client.post("/books/new", json=book_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    created_book = response.json()
    assert created_book["title"] == book_data["title"]
    assert created_book["author"] == book_data["author"]

def test_create_new_lender():
    # Test creating a new lender
    lender_data = {"lender_name": "Test Lender"}
    response = client.post("/lenders/new", json=lender_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    created_lender = response.json()
    assert created_lender["lender_name"] == lender_data["lender_name"]

def test_update_admin_password():
    # new_token = test_create_admin()
    new_password_data = {"password":"new_test_password"}
    response = client.post("/admins/update", json=new_password_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    updated_admin = response.json()
    assert "id" in updated_admin
    assert "username" in updated_admin

if __name__ == '__main__':
    unittest.main()
