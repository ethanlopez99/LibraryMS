import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import main
from api import database
from api.crud import create_admin
from api.security import login

# Replace 'your_database_url' with the actual connection string for your database
DATABASE_URL = "sqlite:///./libraryms.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

main.app.dependency_overrides[database.get_db] = override_get_db
client = TestClient(main.app)

class TestCRUDFunctions(unittest.TestCase):

    # def setUp(self):
    #     # Create tables in the test database
    #     database.Base.metadata.create_all(bind=engine)

    #     admin_data = {"username":"Test Admin 1", "password": "test_password"}
    #     self.test_admin = create_admin(next(override_get_db()), admin_data)
    #     self.access_token = login(next(override_get_db()), admin_data)
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpemFudGVzdCIsImlkIjozfQ.R6mUDW8pJbyv7ekxFFb9POZrLoae9f9xkEy36NvR-s8"}

    # def tearDown(self):
    #     # Drop all tables after the test
    #     database.Base.metadata.drop_all(bind=engine)

    def test_create_admin(self):
        admin_data = {"username": "test_admin1", "password": "test_password"}
        response = client.post("/admins/register", json=admin_data, headers=self.headers)
        print(response)
        self.assertEqual(response.status_code, 200)
        created_admin = response.json()
        self.assertEqual(created_admin["username"], admin_data["username"])

    def test_get_all_admins(self):
        # Assume there is at least one admin in the database
        response = client.get("/admins/" , headers=self.headers)
        self.assertEqual(response.status_code, 200)
        admins = response.json()
        self.assertTrue(len(admins) > 0)

    def test_new_book(self):
        book_data = {"title": "Test Book", "author": "Test Author"}
        response = client.post("/books/new", json=book_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        created_book = response.json()
        self.assertEqual(created_book["title"], book_data["title"])

    def test_get_all_books(self):
        # Assume there is at least one book in the database
        response = client.get("/books/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        books = response.json()
        self.assertTrue(len(books) > 0)

    def test_new_lender(self):
        lender_data = {"lender_name": "Test Lender"}
        response = client.post("/lender/create", json=lender_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        created_lender = response.json()
        self.assertEqual(created_lender["lender_name"], lender_data["lender_name"])

    def test_get_all_lenders(self):
        # Assume there is at least one lender in the database
        response = client.get("/lenders", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        lenders = response.json()
        self.assertTrue(len(lenders) > 0)

    def test_new_transaction(self):
        # Assuming there is at least one book and one lender in the database
        book_data = {"title": "Test Book", "author": "Test Author"}
        response = client.post("/books/new", json=book_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        created_book = response.json()

        lender_data = {"lender_name": "Test Lender"}
        response = client.post("/lenders/new", json=lender_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        created_lender = response.json()

        transaction_data = {"book_id": created_book["id"], "lender_id": created_lender["id"], "transaction_type": 1}
        response = client.post("/transactions", json=transaction_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        created_transaction = response.json()
        self.assertEqual(created_transaction["book_id"], transaction_data["book_id"])

        transaction_data = {"book_id": created_book["id"], "lender_id": created_lender["id"], "transaction_type": 0}
        response = client.post("/transactions", json=transaction_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        created_transaction = response.json()
        self.assertEqual(created_transaction["book_id"], transaction_data["book_id"])

    def test_get_transactions(self):
        # Assume there is at least one transaction in the database
        response = client.get("/transactions", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        transactions = response.json()
        self.assertTrue(len(transactions) > 0)

if __name__ == '__main__':
    unittest.main()
