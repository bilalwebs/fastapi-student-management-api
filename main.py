# main.py
from fastapi import FastAPI
from routers.students import router
import models

from database import Base, engine


app = FastAPI()


# Table create
Base.metadata.create_all(bind=engine)


# router
app.include_router(router)
