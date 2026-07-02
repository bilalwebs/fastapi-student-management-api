

# routers/students.py
from fastapi import APIRouter, Depends, HTTPException, status
from fake_data import students
# API Validation
from model import (Student, StudentCreateResponse,
                   StudentDeleteResponse, StudentResponse, StudentUpdateResponse)
from dependencies import verify_user

# Database Table
from models import Student as StudentModel

from sqlalchemy.orm import Session
from database import get_db

# Sorting
from sqlalchemy import asc, desc


# router = APIRouter()
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# ! GET ALL STUDENTS
# @app.get("/students")
# async def get_students(
#         sort_by: str | None = None, order: str = "asc"):
#     return {
#         "sort_by": sort_by,
#         "order": order
#     }

# @app.get("/students")
# async def get_students(
#         name: str | None = None):
#     result = []
#     for std in students:
#         if name is None or name.lower() in std['name'].lower():
#             result.append(std)
#     return {"students": result}


# @app.get("/students")
# @router.get("", response_model=list[StudentResponse])
# async def get_students(
#     db: Session = Depends(get_db),
#     user: dict = Depends(verify_user),

#     department: str | None = None,
#     age: int | None = None,
#     name: str | None = None,

#     sort_by: str | None = None,
#     order: str = "asc",

#     skip: int = 0,
#     limit: int = 100

# ):
#     print(user)
#     result = []

#     # =========================================================
#     # FILTER + SEARCH
#     # =========================================================
#     for std in students:
#         if (
#             (department is None or std["department"].lower(
#             ) == department.lower())
#             and
#             (age is None or std["age"] == age)
#             and
#             (name is None or name.lower() in std["name"].lower())
#         ):
#             result.append(std)

#     # =========================================================
#     # SORTING
#     # =========================================================

#     # Sirf in fields par sorting allow hogi
#     allowed_fields = ["id", "name", "age", "department"]

#     if sort_by:

#         # Agar user invalid field bhejta hai
#         if sort_by not in allowed_fields:
#             # return {
#             #     "error": "Invalid sort field",
#             #     "allowed_fields": allowed_fields
#             # }

#             # Old Method
#             # raise HTTPException(
#             #     status_code=400,
#             #     detail=f"Invalid sort field. Allowed fields are: {allowed_fields}"
#             # )

#             # Professional Method
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"Invalid sort field. Allowed fields are: {allowed_fields}"
#             )

#         # Valid field ho to sorting karo
#         result = sorted(
#             result,
#             key=lambda std: std[sort_by]
#         )

#         # Descending order
#         if order.lower() == "desc":
#             result.reverse()

#     # =========================================================
#     # PAGINATION
#     # =========================================================

#     result = result[skip: skip + limit]

#     # return {"students": result}
#     return result

@router.get("", response_model=list[StudentResponse])
async def get_students(db: Session = Depends(get_db),
                       user: dict = Depends(verify_user),


                       name: str | None = None,
                       age: int | None = None,
                       department: str | None = None,

                       skip: int = 0,
                       limit: int = 100,

                       sort_by: str | None = None,
                       order: str = "asc"
                       ):
    # students = db.query(StudentModel).all()
    # return students

    query = db.query(StudentModel)

    # Filtering
    if name:
        query = query.filter(StudentModel.name.ilike(f"%{name}%"))

    if age:
        query = query.filter(StudentModel.age == age)

    if department:
        query = query.filter(StudentModel.department.ilike(f"%{department}%"))

    # Sorting
    allowed_fields = {
        "id": StudentModel.id,
        "name": StudentModel.name,
        "age": StudentModel.age,
        "department": StudentModel.department

    }
    if sort_by:
        if sort_by not in allowed_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field. Allowed fields are: {list(allowed_fields.keys())}"
            )

        sort_column = allowed_fields[sort_by]

        if order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

    # limit and skip for pagination

    query = query.offset(skip).limit(limit)

    students = query.offset(skip).limit(limit).all()
    return students


# ! POST (ADD STUDENT)
# @app.post("/students", status_code=201) # status_code=201 is perfect

# @router.post(
#     "",
#     status_code=status.HTTP_201_CREATED,  # Professional
#     response_model=StudentCreateResponse
# )
# async def create_student(student: Student, user: dict = Depends(verify_user)):

#     # model -> dict
#     student_dict = student.model_dump()

#     # id generate
#     if students:
#         student_dict['id'] = max(std['id'] for std in students) + 1
#     else:
#         student_dict['id'] = 1

#     # add to list
#     students.append(student_dict)
#     print(user)
#     return {
#         "message": "Student created successfully",
#         "student": student_dict
#     }


@router.post("", status_code=status.HTTP_201_CREATED,
             response_model=StudentCreateResponse)
async def create_student(
    student: Student,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_user)
):
    student_db = StudentModel(
        name=student.name,
        age=student.age,
        email=student.email,
        department=student.department,
        password=student.password
    )

    db.add(student_db)
    db.commit()
    db.refresh(student_db)

    return {
        "message": "Student created successfully",
        "student": student_db
    }

# ! GET SINGLE STUDENT (BY ID)


# @router.get("/{student_id}", response_model=StudentResponse)
# async def get_student(student_id: int, user: dict = Depends(verify_user)):

#     print(user)
#     for std in students:
#         if std["id"] == student_id:
    # return {"student": std} not included response_model
    # return std  # include response model

    # * Old Method
    # * return {"error": "Student not found"}

    # * status_code=404

    # * Professional Method
    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail="Student not found."
    # )


# !db query use
@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int,
                      db: Session = Depends(get_db),
                      user: dict = Depends(verify_user)
                      ):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    return student


# ! PUT update Data
# @app.put("/students/{student_id}")
# @router.put(
#     "/{student_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=StudentUpdateResponse
# )
# async def update_student(student_id: int, student: Student, user: dict = Depends(verify_user)):
#     print(user)
#     for std in students:
#         if std["id"] == student_id:
#             std['name'] = student.name
#             std['age'] = student.age
#             std['department'] = student.department
#             std['password'] = student.password
#             std['email'] = student.email

#             return {
#                 "message": "Student update successfully",
#                 "student": std
#             }

    # Old Method
    # return {"error": "Student not found"}

    # status_code=404

    # * Professional Method
    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail="Student not found."
    # )

#! db user put
@router.put(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=StudentUpdateResponse
)
async def update_student(
    student_id: int,
    student: Student,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_user)
):
    student_db = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if not student_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    student_db.name = student.name
    student_db.age = student.age
    student_db.email = student.email
    student_db.department = student.department
    student_db.password = student.password

    db.commit()
    db.refresh(student_db)

    return {
        "message": "Student updated successfully",
        "student": student_db
    }


# ! DELETE
# @app.delete("/students/{student_id}")
# @router.delete(
#     "/{student_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=StudentDeleteResponse
# )
# async def delete_student(student_id: int, user: dict = Depends(verify_user)):
#     print(user)
#     for std in students:
#         if std["id"] == student_id:
#             students.remove(std)
#             return {
#                 "message": "Student deleted successfully",
#                 "student": std
#             }

#     # Old Method
#     # return {"error": "Student not found"}

#     # status_code=404

#     # Professional Method
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Student not found."
#     )


# ! delete db use
@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=StudentDeleteResponse
)
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_user)
):
    student_db = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if not student_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    db.delete(student_db)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student": student_db
    }
