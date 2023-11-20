from fastapi import FastAPI

import databases
from api import models, admins
from api.database import Base, engine

app = FastAPI()

app.include_router(admins.router)


# Create tables
Base.metadata.create_all(bind=engine)