"""
===============================================================================
DATABASE.PY
This file sets up the connection to the PostgreSQL database.
It uses SQLAlchemy to create a bridge so our Python code can talk to the database.
===============================================================================
"""

import os

# load_dotenv reads the secret variables from your .env file
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load the environment variables (like the database password) into Python
load_dotenv()

# Get the database connection string from the .env file
DATABASE_URL = os.environ["DATABASE_URL"]

# 1. THE ENGINE
# The engine is the actual connection to the database. 
# It handles the physical communication with PostgreSQL.
engine = create_engine(DATABASE_URL)

# 2. THE SESSION
# A session is like a single "conversation" with the database.
# When a user makes a request, we open a session, ask for data, and then close it.
SessionLocal = sessionmaker(
    autocommit=False, # We want to manually save (commit) changes
    autoflush=False,  # We want to manually push changes
    bind=engine       # Connect this session maker to our engine
)

# 3. THE BASE
# This is a base class that all our database models (tables) will inherit from.
# It helps SQLAlchemy keep track of all the tables we create in models.py.
Base = declarative_base()


def get_db():
    """
    This function creates a new database session for each request.
    Think of it like opening a door to the database, letting the request do its job, 
    and then always remembering to lock the door (close) when finished.
    """
    db = SessionLocal()
    
    try:
        # 'yield' hands the database session to the API route that needs it
        yield db
        
    finally:
        # 'finally' ensures that no matter what happens (even if there is an error),
        # the connection is closed so we don't crash the database with too many open doors.
        db.close()