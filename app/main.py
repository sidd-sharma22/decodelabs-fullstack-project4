"""
===============================================================================
MAIN.PY
This is the starting point of your FastAPI backend! 
When you run the server, this file wakes up first, sets up the database, 
and gets the API ready to receive requests from your frontend.
===============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import engine
from app.routes import router

# ==================================================
# 1. Create Database Tables
# ==================================================
# Before the app even starts, this line tells SQLAlchemy to look at your models.py
# blueprint and build the actual tables in your PostgreSQL database if they don't exist.
models.Base.metadata.create_all(bind=engine)


# ==================================================
# 2. FastAPI Application Setup
# ==================================================
# Here we create the actual API application and give it a name and description.
app = FastAPI(
    title="StudyHub API",
    description="""
    StudyHub Backend API

    Features:
    - User Registration & Login
    - JWT Authentication & Role-Based Authorization
    - Student Task Management
    - PostgreSQL Database Integration
    """,
    version="2.0.0"
)


# ==================================================
# 3. CORS Configuration
# ==================================================
# CORS stands for Cross-Origin Resource Sharing. 
# By default, browsers block websites from talking to APIs on different ports.
# This middleware is like a bouncer at a club saying: "It's okay, let the frontend in!"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows requests from any frontend URL (good for development)
    allow_credentials=True,
    allow_methods=["*"], # Allows all actions like GET, POST, PUT, DELETE
    allow_headers=["*"], # Allows all types of headers
)


# ==================================================
# 4. Register API Routes
# ==================================================
# This tells the Main Manager to pass all the incoming traffic to the 
# Traffic Cop (router) we created in routes.py.
app.include_router(router)


# ==================================================
# 5. Health Check Route
# ==================================================
@app.get("/")
def home():
    """
    A simple health check endpoint. 
    If you visit the base URL (http://127.0.0.1:8000/), this proves the server is alive!
    """
    return {
        "message": "Welcome to the StudyHub API!",
        "status": "Server is running perfectly."
    }


# 1. python -m venv venv
# 2. venv\Scripts\activate
# 3. pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
# 4. pip install "pydantic[email]"