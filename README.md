# 🎓 StudyHub - Full Stack Student Productivity Platform

![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-Educational-blue)

A full-stack web application built as part of the DecodeLabs Full Stack Development Internship Program.

StudyHub helps students organize and manage their study tasks through a secure role-based system. The platform includes user authentication, task management, admin controls, and PostgreSQL database integration using FastAPI as the backend and Vanilla JavaScript for the frontend.


##  Live Demo
**Check out the live project here:** [StudyHub Live Demo](https://studyhub-decodelabs.vercel.app/)

## Application Screenshots

### Landing Page

![Landing Page](assests/screenshots/landing-page.png)

### Sign-In/Sign-Up Page

* Register Page

![Register Page](assests/screenshots/register-page.png)

* Login Page

![Login Page](assests/screenshots/login-page.png)

### Student Dashboard

![Student Dashboard](assests/screenshots/student-dashboard.png)

### Admin Dashboard

* Statistical Page

![Admin Dashboard](assests/screenshots/admin-dashboard1.png)

* Task View Page

![Admin Dashboard](assests/screenshots/admin-dashboard2.png)

---

## 📖 Project Overview

StudyHub is designed to give students a simple, secure way to create, track, and update their study tasks. 

**Key Platform Highlights:**
* Secure user authentication using JWT tokens
* Dedicated student dashboard for personal task management
* Comprehensive admin dashboard for platform monitoring
* PostgreSQL database integration with SQLAlchemy ORM
* Strict role-based access control (Student vs. Admin)
* Full CRUD functionality for all resources
* Responsive, mobile-first user interface

This project demonstrates modern full-stack development concepts including frontend-backend integration, authentication, authorization, database management, and API development.

---

## ✨ Features

### 🔒 Authentication & Security
* User Registration & Login
* JWT (JSON Web Token) Authentication
* Password Hashing using `bcrypt`
* Protected API Routes
* Secure Session Management
* Role-Based Authorization

### 👨‍🎓 Student Features
* Create, View, Update, and Delete personal tasks
* Secure Task Ownership Validation (students can only see/edit their own tasks)
* Personalized Productivity Dashboard

### 👑 Admin Features
* View all registered users and global tasks
* Delete any task on the platform
* **Platform Statistics Dashboard:**
  * Total Users Count
  * Total Tasks Count
  * Completed vs. Pending Tasks

---

## 🛠️ Tech Stack

**Frontend**
* HTML5, CSS3, Vanilla JavaScript

**Backend**
* Python 3, FastAPI

**Database & ORM**
* PostgreSQL, SQLAlchemy

**Security & Validation**
* JWT, Passlib (`bcrypt`), Pydantic

**Environment Management**
* `python-dotenv`

---

## 🏗️ Project Architecture

```text
Frontend (HTML/CSS/JS)
          │
          ▼
 FastAPI REST API
          │
          ▼
 PostgreSQL Database
```

---

## 📂 Folder Structure

```text
studyhub/
│
├── app/                  # Backend Application
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── main.py
│
├── pages/                # Frontend Pages
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── admin-dashboard.html
│
├── css/                  # CSS Files
│   ├── admin.css
│   ├── auth.css
│   ├── home.css
│   ├── dashboard.css
│   └── main.css
│
├── js/                   # Frontend Logic
│   ├── auth.js
│   ├── dashboard.js
│   └── admin.js
│
├── assets/               # Resources
│   ├── icons/
│   ├── screenshots/
│   └── images/
│
├── index.html            # Landing Page
├── script.js             # Global Scripts
│
├── .env                  # Environment Variables (Ignored in Git)
├── requirements.txt      # Python Dependencies
└── README.md             # Project Documentation
```

---

## 🗄️ Database Schema

### Users Table

| Column                | Type    |
| --------------------- | ------- |
| ```id```              | Integer |
| ```name```            | String  |
| ```email```           | String  |
| ```hashed_password``` | String  |
| ```role```            | String  |

### Tasks Table

| Column        | Type    |
| ------------- | ------- |
| ```id```      | Integer |
| ```title```   | String  |
| ```status```  | String  |
| ```user_id``` | Integer |

Relationship:

```One User``` ──> ```Many Tasks```


---

## 🔌 API Endpoints

### Authentication

| Method       | Endpoint        | Description   |
| ------------ | --------------- | ------------- |
| ```POST```   | ```/register``` | Register User |
| ```POST```   | ```/login```    | Login User    |
| ```GET```    | ```/me```       | Current User  |

### Student Routes

| Method       | Endpoint             | Description    |
| ------------ | -------------------- | -------------- |
| ```GET```    | ```/my-tasks```      | View Own Tasks |
| ```POST```   | ```/my-tasks```      | Create Task    |
| ```PUT```    | ```/my-tasks/{id}``` | Update Task    |
| ```DELETE``` | ```/my-tasks/{id}``` | Delete Task    |

### Admin Routes

| Method       | Endpoint          | Description        |
| ------------ | ----------------- | ------------------ |
| ```GET```    | ```/users```      | View All Users     |
| ```GET```    | ```/tasks```      | View All Tasks     |
| ```GET```    | ```/tasks/{id}``` | View Specific Task |
| ```DELETE``` | ```/tasks/{id}``` | Delete Any Task    |

### Relationship Routes

| Method       | Endpoint                | Description             |
| ------------ | ----------------------- | ----------------------- |
| ```GET```    | ```/users/{id}/tasks``` | User Tasks              |
| ```GET```    | ```/users/{id}/full```  | User Details With Tasks |

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### 2. Navigate to Project

```bash
cd studyhub
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost/studyhub
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 7. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

### 8. Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

### 9. Run Frontend

Open:

```text
index.html
```

in your browser.

---

## Authentication Flow

```text
Register
    ↓
Login
    ↓
JWT Token Generated
    ↓
Token Stored in Browser
    ↓
Protected API Access
```

---

## Role-Based Access Control

### Student

```text
Create Tasks
View Own Tasks
Update Own Tasks
Delete Own Tasks
```

### Admin

```text
View All Users
View All Tasks
Delete Any Task
Platform Monitoring
Dashboard Statistics
```

---

## 📈 Learning Outcomes

This project helped develop practical experience with:

* Full Stack Development
* FastAPI Framework
* PostgreSQL Database Design
* SQLAlchemy ORM
* REST API Development
* JWT Authentication
* Role-Based Authorization
* Frontend-Backend Integration
* CRUD Operations
* Database Relationships
* Responsive UI Design
* Project Architecture
* API Testing with Swagger

---

## 🚀 Future Improvements

* Email Verification
* Password Reset System
* Task Categories
* Task Priority Levels
* Task Deadlines
* Search & Filtering
* User Profile Management
* Dark Mode
* Pagination
* Docker Deployment
* Cloud Hosting

---

## 🖥️ Internship Context

This project was developed as part of the DecodeLabs Full Stack Development Internship Program.

Project Objectives:

* Frontend Development
* Backend API Development
* Database Integration
* Authentication & Authorization
* Full Stack Integration
* Production-Oriented Development Practices

---

## 👨‍💻 Author

**Siddharth Sharma**  
CSE Student | Full Stack Development Intern - DecodeLabs

---

## 🪪 License

This project was developed for educational and internship purposes.