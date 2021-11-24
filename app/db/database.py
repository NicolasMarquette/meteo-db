"""The postgresql database."""

# import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = 331295
DB_HOST = "20.101.63.152"
DB_PORT = 5432

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
