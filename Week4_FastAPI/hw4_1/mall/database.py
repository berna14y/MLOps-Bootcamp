# This file is part of a project setup for potential future database integration.
# Currently, it is not used as the API developed for homework does not require database interaction.

import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def get_db():
     db = Session(engine)
     try:
         yield db
     finally:
         db.close()

