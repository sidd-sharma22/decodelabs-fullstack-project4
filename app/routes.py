"""
===============================================================================
ROUTES.PY
This file acts as the "Traffic Cop" of your API.
It receives requests from the frontend, checks security permissions, 
calls the right database workers in crud.py, and sends the response back.
===============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import (
    create_access_token,
    get_current_admin,
    get_current_user,
    get_current_student,
    verify_password
)
from app.database import get_db

router = APIRouter()

# ==================================================
# Authentication Routes (Logging in and out)
# ==================================================

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Creates a new user account.
    """
    new_user = crud.register_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    return new_user


@router.post("/login", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Checks the user's email and password, and gives them a digital ID card (JWT token) if correct.
    """
    db_user = crud.get_user_by_email(db, user.email)

    # If the email doesn't exist, stop them
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # If the password doesn't match the scrambled password in the database, stop them
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Success! Create a digital ID card for them
    access_token = create_access_token(
        data={"sub": str(db_user.id), "role": db_user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.CurrentUser)
def get_current_user_info(current_user=Depends(get_current_user)):
    """
    Returns the details of the person currently holding the digital ID card.
    """
    return current_user


# ==================================================
# Admin Routes (Only Admins can use these)
# ==================================================

@router.get("/users", response_model=list[schemas.UserResponse])
def get_users(current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Admin power: See a list of every user registered on the platform.
    """
    return crud.get_users(db)


@router.get("/tasks", response_model=list[schemas.TaskResponse])
def get_all_tasks(current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Admin power: See a list of every task ever created by anyone.
    """
    return crud.get_tasks(db)


@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Admin power: Look at the details of one specific task.
    """
    task = crud.get_task(db, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Admin power: Delete any task from the database.
    """
    deleted_task = crud.delete_task(db, task_id)

    if not deleted_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}


# ==================================================
# Student Routes (Students managing their own stuff)
# ==================================================

@router.get("/my-tasks", response_model=list[schemas.TaskResponse])
def get_my_tasks(current_user=Depends(get_current_student), db: Session = Depends(get_db)):
    """
    Student: See a list of only their own tasks.
    """
    return crud.get_my_tasks(db, current_user["user_id"])


@router.post("/my-tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_my_task(task: schemas.TaskCreate, current_user=Depends(get_current_student), db: Session = Depends(get_db)):
    """
    Student: Create a new task that belongs to them.
    """
    return crud.create_my_task(db, current_user["user_id"], task)


@router.put("/my-tasks/{task_id}", response_model=schemas.TaskResponse)
def update_my_task(task_id: int, task: schemas.TaskCreate, current_user=Depends(get_current_student), db: Session = Depends(get_db)):
    """
    Student: Change the title or status of their own task.
    """
    updated_task = crud.update_my_task(db, task_id, current_user["user_id"], task)

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if updated_task == "forbidden":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this task"
        )

    return updated_task


@router.delete("/my-tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_my_task(task_id: int, current_user=Depends(get_current_student), db: Session = Depends(get_db)):
    """
    Student: Delete one of their own tasks.
    """
    deleted_task = crud.delete_my_task(db, task_id, current_user["user_id"])

    if deleted_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if deleted_task == "forbidden":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this task"
        )

    return {"message": "Task deleted successfully"}


# ==================================================
# Relationship Routes (Connecting Users to Tasks)
# ==================================================

@router.get("/users/{user_id}/tasks", response_model=list[schemas.TaskResponse])
def get_tasks_by_user(user_id: int, current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Admin: See all the tasks that belong to a specific student.
    """
    return crud.get_tasks_by_user(db, user_id)


@router.get("/users/{user_id}/full", response_model=schemas.UserWithTasks)
def get_user_with_tasks(user_id: int, current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Admin: Look up a specific student and see all their details along with all their tasks.
    """
    user = crud.get_user_with_tasks(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user