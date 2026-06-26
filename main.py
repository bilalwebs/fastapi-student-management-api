# main.py
from fastapi import FastAPI
from routers.students import router

app = FastAPI()


# router
app.include_router(router)
