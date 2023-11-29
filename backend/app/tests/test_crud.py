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

def test_login(username = "userroot", password="passwordroot"):
    global test_token
    response = client.post(
        "/admins/login",
        json={"username":f"{username}", "password": f"{password}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    test_token = data["access_token"]
    

def test_create_admin():
    # Standard admin creation
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
    
    # Admin creation verification
    response = client.get(f"/admins/{admin_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == admin_id
    test_login(username="testuser1",password="testpassword1") # For updating password test

def test_create_admin_empty_password():
    # Create admin with empty password
    response = client.post(
        "/admins/register",
        json={"username": "testuser1", "password": ""},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_empty_username():
    # Create admin with empty username
    response = client.post(
        "/admins/register",
        json={"username": "", "password": "testpassword1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_long_username():
    # Create admin with username > 32 characters
    response = client.post(
        "/admins/register",
        json={"username": "testusername1testusername1testusername1", "password": "testpassword1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_long_password():
    # Create admin with password > 32 characters
    response = client.post(
        "/admins/register",
        json={"username": "testusername1", "password": "testpassword1testpassword1testpassword1testpassword1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_short_username():
    # Create admin with username < 8 characters
    response = client.post(
        "/admins/register",
        json={"username": "test1", "password": "testpassword1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_short_password():
    # Create admin with password < 8 characters
    response = client.post(
        "/admins/register",
        json={"username": "testusername1", "password": "test1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_space_username():
    # Create admin with space in username
    response = client.post(
        "/admins/register",
        json={"username": "test user", "password": "testpassword1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_space_password():
    # Create admin with space in password
    response = client.post(
        "/admins/register",
        json={"username": "testusername1", "password": "test password"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_admin_special_chars():
    # Create admin with special characters in username
    response = client.post(
        "/admins/register",
        json={"username": "test&user", "password": "testpassword1"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

    
def test_create_duplicate_admin():
    # create admin with same username as already exists
    response = client.post(
        "/admins/register",
        json={"username": "testuser1", "password": "testpassword2"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 409, response.text

def test_update_admin_password():
    # new_token = test_create_admin()
    new_password_data = {"password":"new_test_password"}
    response = client.post("/admins/update", json=new_password_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    updated_admin = response.json()
    assert "id" in updated_admin
    assert "username" in updated_admin

def test_create_new_book():
    # standard new book request
    book_data = {"title": "Test Book", "author": "Test Author"}
    response = client.post("/books/new", json=book_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    created_book = response.json()
    assert created_book["title"] == book_data["title"]
    assert created_book["author"] == book_data["author"]

def test_create_book_empty_title():
    # create book with empty title
    response = client.post(
        "/books/new",
        json={"title": "", "author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_book_no_title():
    # create book with empty title
    response = client.post(
        "/books/new",
        json={"author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_book_long_title():
    # create book with title > 96 chars
    response = client.post(
        "/books/new",
        json={"title": "testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1", "author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_book_long_author():
    # create book with author > 50 chars
    response = client.post(
        "/books/new",
        json={"title": "Test Book 1", "author": "Test AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_create_book_special_chars_title():
    # create book with special chars in title
    response = client.post(
        "/books/new",
        json={"title": "Test&Book 1", "author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_update_book():
    # create book with special chars in author
    response = client.post(
        "/books/update",
        json={"id": "1","title": "Test Book Updated", "author": "Test Author Updated"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    updated_book = response.json()
    assert updated_book["title"] == "Test Book Updated"
    assert updated_book["author"] == "Test Author Updated"


def test_update_book_empty_title():
    # update book with empty title
    response = client.post(
        "/books/update",
        json={"id":"1", "title": "", "author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_update_book_no_title():
    # update book with empty title
    response = client.post(
        "/books/update",
        json={"id": "1", "author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_update_book_long_title():
    # update book with title > 96 chars
    response = client.post(
        "/books/update",
        json={"id":"1", "title": "testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1testbook1", "author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_update_book_long_author():
    # update book with author > 50 chars
    response = client.post(
        "/books/update",
        json={"id":"1", "title": "Test Book 1", "author": "Test AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest AuthorTest Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text

def test_update_book_special_chars_title():
    # update book with special chars in title
    response = client.post(
        "/books/update",
        json={"id":"1", "title": "Test&Book 1", "author": "Test Author"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422, response.text


def test_create_new_lender():
    # Test creating a new lender
    lender_data = {"lender_name": "Test Lender"}
    response = client.post("/lenders/new", json=lender_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    created_lender = response.json()
    assert created_lender["lender_name"] == lender_data["lender_name"]


if __name__ == '__main__':
    unittest.main()
