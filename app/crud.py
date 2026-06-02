"""
===============================================================================
CRUD.PY
This file contains all the database operations.
CRUD stands for Create, Read, Update, and Delete. 
These functions are the actual workers that talk to your PostgreSQL database.
===============================================================================
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import hash_password


# ==================================================
# User CRUD (Managing Students and Admins)
# ==================================================

def register_user(db: Session, user: schemas.UserRegister):
    """
    Takes the data from the registration form, scrambles the password for safety,
    and saves the brand new student to the database.
    """
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="student" # Everyone who registers is a student by default
    )

    try:
        # Try to save the new user to the database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        
    except IntegrityError:
        # If the email is already in the database, it causes an IntegrityError.
        # We 'rollback' (cancel) the action so the database doesn't crash.
        db.rollback()
        return None


def get_users(db: Session):
    """
    Reads the database and returns a list of every single user.
    """
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    """
    Finds one specific user by their unique ID number.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Finds one specific user by checking if their email matches.
    """
    return db.query(models.User).filter(models.User.email == email).first()


# ==================================================
# Student Task CRUD (Students managing their own tasks)
# ==================================================

def create_my_task(db: Session, user_id: int, task: schemas.TaskCreate):
    """
    Creates a new task and attaches it directly to the logged-in user's ID.
    """
    db_task = models.Task(
        title=task.title,
        status=task.status,
        user_id=user_id # This links the task to the student
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_my_tasks(db: Session, user_id: int):
    """
    Finds all tasks, but filters them so it only returns the ones 
    belonging to the logged-in user.
    """
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()


def update_my_task(db: Session, task_id: int, user_id: int, task: schemas.TaskCreate):
    """
    Updates a task's title or status, but ONLY if the student owns it.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return None

    # Ownership Check: If the person trying to edit this task is not the owner, stop them!
    if db_task.user_id != user_id:
        return "forbidden"

    db_task.title = task.title
    if task.status is not None:
        db_task.status = task.status

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_my_task(db: Session, task_id: int, user_id: int):
    """
    Deletes a task, but ONLY if the student owns it.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return None

    # Ownership Check: Stop them if they don't own it!
    if db_task.user_id != user_id:
        return "forbidden"

    db.delete(db_task)
    db.commit()
    return db_task


# ==================================================
# Admin Task CRUD (Admins have ultimate power)
# ==================================================

def get_tasks(db: Session):
    """
    Admin power: Get every single task in the entire system, regardless of who owns it.
    """
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    """
    Admin power: Look up any specific task by its ID.
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def delete_task(db: Session, task_id: int):
    """
    Admin power: Delete ANY task in the system. Notice there is no "Ownership Check" here!
    """
    db_task = get_task(db, task_id)

    if db_task:
        db.delete(db_task)
        db.commit()

    return db_task


# ==================================================
# Relationship Queries (Connecting Users to Tasks)
# ==================================================

def get_tasks_by_user(db: Session, user_id: int):
    """
    Finds all tasks that belong to a specific user ID.
    """
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()


def get_user_with_tasks(db: Session, user_id: int):
    """
    Finds a specific user, and because of how models.py is set up, 
    it automatically pulls in all of their tasks too!
    """
    return db.query(models.User).filter(models.User.id == user_id).first()