# main.py

from fastapi import FastAPI, HTTPException, status, Depends
from model import Student, StudentResponse, StudentCreateResponse, StudentUpdateResponse, StudentDeleteResponse
from fake_data import students

app = FastAPI()

# dummpy function


def verify_user():
    return {
        "username": "bilal",
        "role": "admin"
    }


@app.get("/")
async def read_root():
    return {"message": "Student Management API CRUD Application"}


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
@app.get("/students", response_model=list[StudentResponse])
async def get_students(
    user: dict = Depends(verify_user),

    department: str | None = None,
    age: int | None = None,
    name: str | None = None,

    sort_by: str | None = None,
    order: str = "asc",

    skip: int = 0,
    limit: int = 100

):
    print(user)
    result = []

    # =========================================================
    # FILTER + SEARCH
    # =========================================================
    for std in students:
        if (
            (department is None or std["department"].lower(
            ) == department.lower())
            and
            (age is None or std["age"] == age)
            and
            (name is None or name.lower() in std["name"].lower())
        ):
            result.append(std)

    # =========================================================
    # SORTING
    # =========================================================

    # Sirf in fields par sorting allow hogi
    allowed_fields = ["id", "name", "age", "department"]

    if sort_by:

        # Agar user invalid field bhejta hai
        if sort_by not in allowed_fields:
            # return {
            #     "error": "Invalid sort field",
            #     "allowed_fields": allowed_fields
            # }

            # Old Method
            # raise HTTPException(
            #     status_code=400,
            #     detail=f"Invalid sort field. Allowed fields are: {allowed_fields}"
            # )

            # Professional Method
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field. Allowed fields are: {allowed_fields}"
            )

        # Valid field ho to sorting karo
        result = sorted(
            result,
            key=lambda std: std[sort_by]
        )

        # Descending order
        if order.lower() == "desc":
            result.reverse()

    # =========================================================
    # PAGINATION
    # =========================================================

    result = result[skip: skip + limit]

    # return {"students": result}
    return result


# ! POST (ADD STUDENT)
# @app.post("/students", status_code=201) # status_code=201 is perfect

@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,  # Professional
    response_model=StudentCreateResponse
)
async def create_student(student: Student, user: dict = Depends(verify_user)):

    # model -> dict
    student_dict = student.model_dump()

    # id generate
    if students:
        student_dict['id'] = max(std['id'] for std in students) + 1
    else:
        student_dict['id'] = 1

    # add to list
    students.append(student_dict)
    print(user)
    return {
        "message": "Student created successfully",
        "student": student_dict
    }


# ! GET SINGLE STUDENT (BY ID)
@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, user: dict = Depends(verify_user)):
    print(user)
    for std in students:
        if std["id"] == student_id:
            # return {"student": std} not included response_model
            return std  # include response model

    # Old Method
    # return {"error": "Student not found"}

    # status_code=404

    # Professional Method
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found."
    )


# ! PUT update Data
# @app.put("/students/{student_id}")

@app.put(
    "/students/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=StudentUpdateResponse
)
async def update_student(student_id: int, student: Student, user: dict = Depends(verify_user)):
    print(user)
    for std in students:
        if std["id"] == student_id:
            std['name'] = student.name
            std['age'] = student.age
            std['department'] = student.department
            std['password'] = student.password
            std['email'] = student.email

            return {
                "message": "Student update successfully",
                "student": std
            }

    # Old Method
    # return {"error": "Student not found"}

    # status_code=404

    # Professional Method
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found."
    )

# ! DELETE
# @app.delete("/students/{student_id}")


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=StudentDeleteResponse
)
async def delete_student(student_id: int, user: dict = Depends(verify_user)):
    print(user)
    for std in students:
        if std["id"] == student_id:
            students.remove(std)
            return {
                "message": "Student deleted successfully",
                "student": std
            }

    # Old Method
    # return {"error": "Student not found"}

    # status_code=404

    # Professional Method
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found."
    )
