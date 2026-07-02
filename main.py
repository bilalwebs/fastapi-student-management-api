from fastapi import FastAPI
from routers.students import router
import models

from database import Base, engine

app = FastAPI(
    title="Student Management API",
    description="FastAPI CRUD with SQLAlchemy",
    version="1.0.0"
)

# Create Database Tables
Base.metadata.create_all(bind=engine)


# Root Endpoint
@app.get("/")
async def home():
    return {
        "message": "Welcome to Student Management API",
        "docs": "/docs",
        "students_api": "/students"
    }


# Include Router
app.include_router(router)
