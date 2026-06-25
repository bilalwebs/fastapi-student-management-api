
# model.py
from pydantic import BaseModel

# Request Model


class Student(BaseModel):
    name: str
    age: int
    department: str
    email: str
    password: str


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
