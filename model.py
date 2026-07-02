
# model.py
import re

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

# Request Model


class Student(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=18, le=50)
    department: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    @field_validator("department")
    @classmethod
    def validate_department(cls, value):
        allowed_departments = ["CS", "AI", "SE", "MBS"]
        if value not in allowed_departments:
            raise ValueError(
                f"Department must be one of {allowed_departments}")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter.")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")

        if not re.search(r"[@$!%*?&#]", value):
            raise ValueError(
                "Password must contain at least one special character.")

        return value

    @field_validator("name")
    @classmethod
    def name_validate(cls, value):
        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValueError("Name must contain only letters and spaces.")

        return value


# Single Student Response
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str

    model_config = ConfigDict(from_attributes=True)


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
