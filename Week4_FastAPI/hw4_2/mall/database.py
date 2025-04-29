import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if DATABASE_URL is None:  # Check if DATABASE_URL is set
    raise ValueError("DATABASE_URL environment variable is not set. Check your .env file.")

engine = create_engine(DATABASE_URL, echo=False)

def get_db():
    with Session(engine) as session:
        yield session