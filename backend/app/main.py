from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import databases
from api import models, admins, transactions, books, lenders
from api.database import Base, engine

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

app.include_router(admins.router)
app.include_router(transactions.router)
app.include_router(books.router)
app.include_router(lenders.router)


# Create tables
Base.metadata.create_all(bind=engine)