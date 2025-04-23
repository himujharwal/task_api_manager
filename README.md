
# Flask Task Manager API

A simple REST API to handle **user registration, login, and task management** with **JWT-based authentication** and **role-based access control** (admin, special user, normal user).


## Features

- User **registration** (`/register`)
- User **login** and **JWT token generation** (`/login`)
- **Create tasks** (only authenticated users)
- **View all users' tasks** (admin only)
- **View own tasks** by user ID
- **Update** and **delete tasks** (special users only)

## Setup Instructions

1. Clone the repository.
2. Activate a virtual environment for better experience.
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Setup config file (for example):

    ```python
    import os

    class Config:
        SECRET_KEY = "write any random string here"
        SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```

5. Run the app:

    ```bash
    python run.py
    ```

---



## Endpoints samples

### 1. User Registration
- `POST /register`
- Request body:

  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "user_type": "admin" | "special" | "normal"
  }
  ```
- Response: User created.

---

### 2. User Login
- `POST /login`
- Request body:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- Response: Returns JWT token.

---

### 3. Create Tasks
- `POST /tasks`
- Headers: `Authorization: Bearer <JWT Token>`
- Request body:
  ```json
  {
    "tasks": [
      {"title": "Study Flask", "status": "pending"},
      {"title": "Complete assignment", "status": "processing"},
      {"title": "Submit project", "status": "completed"}
    ]
  }
  ```
- Response: Tasks created for the user.

---

### 4. View All Users' Tasks (Admin Only)
- `GET /tasks`
- Headers: `Authorization: Bearer <JWT Token>` (must be **admin** user)
- Response: List of all users with their tasks.

---

### 5. View Own Tasks by ID
- `GET /tasks/<user_id>`
- Headers: `Authorization: Bearer <JWT Token>`
- Response: List of tasks for the given user if authorized.

---

### 6. Update Task (Special User Only)
- `PUT /tasks/<task_id>`
- Headers: `Authorization: Bearer <JWT Token>` (must be **special** user)
- Request body (any field can be updated):
  ```json
  {
    "title": "New Title",
    "status": "completed"
  }
  ```
- Response: Task updated.

---

### 7. Delete Task (Special User Only)
- `DELETE /tasks/<task_id>`
- Headers: `Authorization: Bearer <JWT Token>` (must be **special** user)
- Response: Task deleted.

---



---

## Notes

- Passwords are **hashed** before storing.
- **JWT token** is used for authentication.
- **Role-based access** ensures different permissions for `admin`, `special`, and `normal` users.
- Token must be sent in the **Authorization header** as:  
  ```
  Authorization: Bearer <your_token>
  ```
- Test APIs using **Postman**

