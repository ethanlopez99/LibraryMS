from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel
from .database import Base


# Admin object created as a table in database. Used by staff, not lenders.
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) # this is already hashed

class AdminCreate(BaseModel):
    username: str
    password: str

# Book object created as a table in database. Each book object will only have 1 lender at any given time.
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(96), unique=True, index=True) # Max length calculated at 5 words title + 7 words subtitle, each word 8 letters
    author = Column(String(50))
    is_available = Column(Boolean, default=True)
    lender_id = Column(Integer, ForeignKey('lenders.id'))

    # Create relationship with Lender object, so can navigate to Lender object from Book object
    lender = relationship("Lender", back_populates="books")


class BookCreate(BaseModel):
    title: str
    author: str
    lender_id: str


# Lender object created as a table in database. Each lender object can have multiple books.
class Lender(Base):
    __tablename__ = "lenders"

    id = Column(Integer, primary_key=True, index=True)
    lender_name = Column(String(32), index=True)

    # Create relationship with Book object, so can navigate to Book object(s) from Lender object
    books = relationship("Book", back_populates="lender")
    
class LenderCreate(BaseModel):
    lender_name: str

class Token(BaseModel):
    access_token: str
    token_type: str