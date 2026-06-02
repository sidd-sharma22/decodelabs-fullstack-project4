"""
===============================================================================
MODELS.PY
This file defines the structure of your database tables using SQLAlchemy.
Think of models as the blueprints for your database.
===============================================================================
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """
    The blueprint for the "users" table.
    This stores all the information about students and admins.
    """
    # The actual name of the table in the PostgreSQL database
    __tablename__ = "users"

    # The unique ID number for each user (Primary Key)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # The user's full name
    name: Mapped[str] = mapped_column(String, nullable=False)

    # The user's email address (must be unique, no two users can have the same email)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # The scrambled security password
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # The role of the user, which defaults to "student" if not specified
    role: Mapped[str] = mapped_column(String, default="student")

    # The Relationship: A user can have many tasks. 
    # cascade="all, delete" means if we delete a user account, all their tasks 
    # get deleted automatically so we don't leave junk in the database!
    tasks = relationship("Task", back_populates="owner", cascade="all, delete")


class Task(Base):
    """
    The blueprint for the "tasks" table.
    This stores all the study tasks created by users.
    """
    # The actual name of the table in the PostgreSQL database
    __tablename__ = "tasks"

    # The unique ID number for each task
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # The title or description of the task
    title: Mapped[str] = mapped_column(String, nullable=False)

    # The current status of the task, which defaults to "Pending"
    status: Mapped[str] = mapped_column(String, default="Pending")

    # The Foreign Key: This links the task back to the specific user's ID who created it
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # The Relationship: This points back to the User model so the code knows who the "owner" is
    owner = relationship("User", back_populates="tasks")