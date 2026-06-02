"""
===============================================================================
AUTH.PY
This file handles security: checking passwords, creating digital "ID cards" 
(JWT tokens), and making sure users only see what they are allowed to see.
===============================================================================
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Any

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# ==================================================
# Environment Variables
# ==================================================
# Load secret settings (like your secret key) from the .env file
load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

# Set how long the token (ID card) is valid. Default is 60 minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# ==================================================
# OAuth2 Configuration
# ==================================================
# This tells FastAPI where the login page is, so it knows where to get the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ==================================================
# Password Hashing
# ==================================================
# We use 'bcrypt' to scramble passwords so even if a hacker steals the database, 
# they cannot read the real passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Takes a normal password and scrambles it into a secure hash.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the entered password matches the scrambled password in the database.
    """
    return pwd_context.verify(plain_password, hashed_password)

# ==================================================
# JWT Functions (Digital ID Cards)
# ==================================================

def create_access_token(data: dict[str, Any]) -> str:
    """
    Creates a JWT token (a temporary digital ID card) after a successful login.
    """
    to_encode = data.copy()
    
    # Calculate exactly when this token should expire so it doesn't last forever
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Create the secure token using our secret key
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict[str, Any]:
    """
    Reads the digital ID card (token) to make sure it is valid and hasn't been faked.
    """
    try:
        # Try to decode the token using our secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("sub")
        role = payload.get("role")
        
        # If there is no user ID inside, the token is broken
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            
        return {
            "user_id": int(user_id),
            "role": role
        }
        
    except JWTError:
        # If the token is expired or tampered with, kick them out
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# ==================================================
# Authentication Dependencies (Security Guards)
# ==================================================

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    """
    The main security guard. It checks the token for EVERY protected route.
    """
    return verify_token(token)

def get_current_admin(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    """
    A strict security guard. It only lets Admins pass through.
    """
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def get_current_student(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    """
    A friendly security guard. It lets both Students and Admins pass through.
    """
    if current_user["role"] not in ["student", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )
    return current_user