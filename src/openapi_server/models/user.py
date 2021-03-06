# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401

from sqlmodel import SQLModel, Field

from humps import camelize



def to_camel(string):
    return camelize(string)

class User(SQLModel, table=True):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    User - a model defined in OpenAPI

        id: The id of this User [Optional].
        username: The username of this User [Optional].
        first_name: The first_name of this User [Optional].
        last_name: The last_name of this User [Optional].
        email: The email of this User [Optional].
        phone: The phone of this User [Optional].
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    @validator("username")
    def username_max_length(cls, value):
        assert len(value) <= 256
        return value

User.update_forward_refs()
