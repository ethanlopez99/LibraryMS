from fastapi import FastAPI

import databases
from api import models, admins, transactions, books, lenders
from api.database import Base, engine

app = FastAPI()

app.include_router(admins.router)
app.include_router(transactions.router)
app.include_router(books.router)
app.include_router(lenders.router)


# Create tables
Base.metadata.create_all(bind=engine)