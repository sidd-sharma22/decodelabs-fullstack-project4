"""
===============================================================================
SCHEMAS.PY
These are Pydantic models (schemas). 
Think of them as "molds" or "filters" for your data. 
They validate incoming data from the frontend and shape the outgoing data.
===============================================================================
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

# ==================================================
# Authentication Schemas (For Logging In & Signing Up)
# ==================================================

class UserRegister(BaseModel):
    """
    Checks the data when a new user tries to register.
    It ensures the name is between 2 and 50 characters, 
    the email is a valid email format, and the password is at least 6 characters.
    """
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """
    Checks the data when a user tries to log in.
    We just need a valid email format and a password string.
    """
    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Shapes the response when a login is successful.
    It sends back the security token and the type of token (Bearer).
    """
    access_token: str
    token_type: str


class CurrentUser(BaseModel):
    """
    Shapes the data when the frontend asks "Who is currently logged in?"
    """
    user_id: int
    role: str


# ==================================================
# User Schemas (For Viewing User Details)
# ==================================================

class UserResponse(BaseModel):
    """
    Shapes the data when sending user details back to the frontend.
    Notice we DO NOT include the password here for security reasons!
    """
    id: int
    name: str
    email: str
    role: str

    class Config:
        # This tells Pydantic to read data even if it comes from an ORM (like SQLAlchemy)
        from_attributes = True


# ==================================================
# Task Schemas (For Creating & Viewing Tasks)
# ==================================================

class TaskCreate(BaseModel):
    """
    Checks the data when a student creates a new task.
    The title must be between 3 and 100 characters. 
    Status is optional and defaults to "Pending".
    """
    title: str = Field(..., min_length=3, max_length=100)
    status: Optional[str] = "Pending"


class TaskResponse(BaseModel):
    """
    Shapes the data when sending a single task back to the frontend.
    It includes the task ID and the ID of the user who owns it.
    """
    id: int
    title: str
    status: str
    user_id: int

    class Config:
        from_attributes = True


class TaskMini(BaseModel):
    """
    A smaller, nested task model used when we are showing a User 
    and all of their tasks together. We don't need the user_id here 
    because we already know who the user is.
    """
    id: int
    title: str
    status: str

    class Config:
        from_attributes = True


class UserWithTasks(BaseModel):
    """
    Shapes the data for the Admin when they want to see a User 
    and a list of every task that user has created.
    """
    id: int
    name: str
    email: str
    tasks: List[TaskMini] = []  # A list of those mini tasks

    class Config:
        from_attributes = True