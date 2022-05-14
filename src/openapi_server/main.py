# coding: utf-8

"""
    User Service

    This is simple client API 

    The version of the OpenAPI document: 1.0.0
    Contact: schetinnikov@gmail.com
    Generated by: https://openapi-generator.tech
"""


from fastapi import FastAPI

from apis.user_api import router as UserApiRouter
from db import init_db

from models.user import User


app = FastAPI(
    title="User Service",
    description="This is simple client API ",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(UserApiRouter)
