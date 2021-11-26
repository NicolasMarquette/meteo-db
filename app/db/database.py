"""The postgresql database."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = Session()

# Dependency
def get_db():
    """Function to connect to the database."""
    db_session = SessionLocal
    try:
        yield db_session
    finally:
        db_session.close()
