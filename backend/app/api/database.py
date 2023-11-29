from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


DATABASE_URL = "sqlite:///./libraryms.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Used to create new sessions of database for each request, to manage lifecycle of db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()