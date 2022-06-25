# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    HTTPException,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)
from fastapi.responses import JSONResponse


from models.extra_models import TokenModel  # noqa: F401
from models.error import Error
from models.user import User

from sqlalchemy import select
from sqlmodel import Session

from keycloak import KeycloakAdmin



router = APIRouter()


@router.post(
    "/user",
    responses={
        200: {"description": "successful operation"},
        500: {"model": Error, "description": "unexpected error"},
    },
    tags=["user"],
    summary="Create user",
)
async def create_user(
    user: User = Body(None, description="Created user object"),
) -> None:
    """This can only be done by the logged in user."""
    try:
        keycloak_admin = KeycloakAdmin(server_url="http://keycloak.localhost/",
                               username='api',
                               password='123123',
                               realm_name="otus")
        new_user = keycloak_admin.create_user({
            "email": user.email,
            "username": user.username,
            "credentials": [{"value": user.password, "type": "password",}],
            "enabled": True,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "attributes": {
                "phone": user.phone
            }
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=Error(code=500, message=str(e)).json(),
        )


@router.delete(
    "/user/{username}",
    responses={
        204: {"description": "user deleted"},
        500: {"model": Error, "description": "unexpected error"},
    },
    tags=["user"],
)
async def delete_user(
    username: str = Path(None, description="username"),
) -> None:
    """deletes a single user based on the username supplied"""
    try:
        keycloak_admin = KeycloakAdmin(server_url="http://keycloak.localhost/",
                               username='api',
                               password='123123',
                               realm_name="otus")
        user_id = keycloak_admin.get_user_id(username=username)
        keycloak_admin.delete_user(user_id)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=Error(code=500, message=str(e)).json(),
        )

@router.get(
    "/user/{username}",
    responses={
        200: {"model": User, "description": "user response"},
        500: {"model": Error, "description": "unexpected error"},
    },
    tags=["user"],
)
async def find_user_by_username(
    username: str = Path(None, description="Username"),
) -> User:
    """Returns a user based on a single ID, if the user does not have access to the user"""

    try:
        keycloak_admin = KeycloakAdmin(server_url="http://keycloak.localhost/",
                               username='api',
                               password='123123',
                               realm_name="otus")
        user_id = keycloak_admin.get_user_id(username=username)
        user = keycloak_admin.get_user(user_id)
        return User(
            username=user["username"],
            first_name=user["firstName"],
            last_name=user["lastName"],
            email=user["email"],
            phone=user["attributes"]["phone"]
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=Error(code=500, message=str(e)).json(),
        )


@router.put(
    "/user/{username}",
    responses={
        200: {"description": "user updated"},
        500: {"model": Error, "description": "unexpected error"},
    },
    tags=["user"],
)
async def update_user(
    username: str = Path(None, description="username"),
    user: User = Body(None, description=""),
) -> None:
    """Update user with username supplied"""
    try:
        keycloak_admin = KeycloakAdmin(server_url="http://keycloak.localhost/",
                               username='api',
                               password='123123',
                               realm_name="otus")
        user_id = keycloak_admin.get_user_id(username=username)

        updated_payload = {}

        if user.email:
            updated_payload["email"] = user.email
        if user.username:
            updated_payload["username"] = user.username
        if user.first_name:
            updated_payload["firstName"] = user.first_name
        if user.last_name:
            updated_payload["lastName"] = user.last_name
        if user.phone:
            updated_payload["attributes"] = { "phone": user.phone }

        keycloak_admin.update_user(user_id, updated_payload)

        if user.password:
            keycloak_admin.set_user_password(user_id=user_id, password=user.password, temporary=False)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=Error(code=500, message=str(e)).json(),
        )
