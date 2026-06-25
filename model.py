
# model.py
from pydantic import BaseModel, EmailStr, Field

# Request Model


class Student(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=18, le=50)
    department: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


# Single Student Response
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str


# POST Response
class StudentCreateResponse(BaseModel):
    message: str
    student: StudentResponse


# Wrapper Response Model (GET ALL)
class StudentsResponse(BaseModel):
    students: list[StudentResponse]

# PUT Response


class StudentUpdateResponse(BaseModel):
    message: str
    student: StudentResponse

# DELETE Response


class StudentDeleteResponse(BaseModel):
    message: str
    student: StudentResponse
