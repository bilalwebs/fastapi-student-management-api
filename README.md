# Student Management API

A beginner-friendly Student Management REST API built with **FastAPI**. This project demonstrates CRUD operations, filtering, searching, sorting, pagination, proper HTTP status codes, exception handling, and **Response Models** using in-memory fake data.

---

## Features

* Create Student
* Get All Students
* Get Student by ID
* Update Student
* Delete Student
* Filter by Department
* Filter by Age
* Search by Name
* Sort by ID, Name, Age, or Department
* Ascending & Descending Sorting
* Pagination (Skip & Limit)
* HTTP Status Codes
* HTTPException Handling
* Pydantic Request Models
* Pydantic Response Models
* Hide Sensitive Data (Email & Password) using Response Models

---

## Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn

---

## Project Structure

```text
.
├── main.py
├── model.py
├── fake_data.py
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/your-username/student-management-api-crud.git
```

Move into the project

```bash
cd student-management-api-crud
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

Run the server

```bash
uvicorn main:app --reload
```

---

## API Documentation

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Get All Students

```
GET /students
```

### Create Student

```
POST /students
```

### Get Student by ID

```
GET /students/{student_id}
```

### Update Student

```
PUT /students/{student_id}
```

### Delete Student

```
DELETE /students/{student_id}
```

---

## Query Parameters

### Filter by Department

```
GET /students?department=CS
```

### Filter by Age

```
GET /students?age=20
```

### Search by Name

```
GET /students?name=ali
```

### Sort by Age

```
GET /students?sort_by=age
```

### Descending Order

```
GET /students?sort_by=age&order=desc
```

### Pagination

```
GET /students?skip=0&limit=2
```

### Combined Query

```
GET /students?department=CS&sort_by=age&order=desc&skip=0&limit=1
```

---

## Sample Request

```json
{
    "name": "Ali",
    "age": 20,
    "department": "CS",
    "email": "ali@gmail.com",
    "password": "Ali12345"
}
```

---

## Sample Response

```json
{
    "message": "Student created successfully",
    "student": {
        "id": 1,
        "name": "Ali",
        "age": 20,
        "department": "CS"
    }
}
```

> **Note:** Email and Password are accepted in the request but are automatically hidden in the API response using **Response Models**.

---

## Status Codes

| Status Code | Description |
| ----------- | ----------- |
| 200         | OK          |
| 201         | Created     |
| 400         | Bad Request |
| 404         | Not Found   |

---

## Concepts Covered

* FastAPI CRUD Operations
* Path Parameters
* Query Parameters
* Filtering
* Searching
* Sorting
* Pagination
* Request Body Validation
* Pydantic Models
* Response Models
* HTTPException
* HTTP Status Codes

---

## Future Improvements

* Pydantic Field Validation
* SQLAlchemy ORM
* SQLite / PostgreSQL
* JWT Authentication
* User Login & Registration
* Dependency Injection
* APIRouter
* Modular Project Structure
* Unit Testing
* Docker Support

---

## Author

**Muhammad Bilal Hussain**

Learning FastAPI step by step by building practical and professional REST APIs.
