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

from db import get_session
from sqlalchemy import select
from sqlmodel import Session



router = APIRouter()


@router.post(
    "/user",
    responses={
        200: {"description": "successful operation"},
    },
    tags=["user"],
    summary="Create user",
)
async def create_user(
    user: User = Body(None, description="Created user object"),
    session: Session = Depends(get_session)
) -> None:
    """This can only be done by the logged in user."""
    session.add(user)
    session.commit()


@router.delete(
    "/user/{userId}",
    responses={
        204: {"description": "user deleted"},
        500: {"model": Error, "description": "unexpected error"},
    },
    tags=["user"],
)
async def delete_user(
    userId: int = Path(None, description="ID of user"),
    session: Session = Depends(get_session)
) -> None:
    """deletes a single user based on the ID supplied"""
    try:
        result = session.query(User).filter(User.id == userId).first()
        session.delete(result)
        session.commit()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=Error(code=500, message="unexpected error").json(),
        )

@router.get(
    "/user/{userId}",
    responses={
        200: {"model": User, "description": "user response"},
        500: {"model": Error, "description": "unexpected error"},
    },
    tags=["user"],
)
async def find_user_by_id(
    userId: int = Path(None, description="ID of user"),
    session: Session = Depends(get_session)
) -> User:
    """Returns a user based on a single ID, if the user does not have access to the user"""
    try:
        result = session.execute(select(User).where(User.id == userId)).one()
        return result[0]
    except:
        return JSONResponse(
            status_code=500,
            content=Error(code=500, message="unexpected error").json(),
        )


@router.put(
    "/user/{userId}",
    responses={
        200: {"description": "user updated"},
        500: {"model": Error, "description": "unexpected error"},
    },
    tags=["user"],
)
async def update_user(
    userId: int = Path(None, description="ID of user"),
    user: User = Body(None, description=""),
    session: Session = Depends(get_session)
) -> None:
    """Update user with User ID supplied"""
    try:
        user_old = session.query(User).filter(User.id == userId).first()

        user_old.username = user.username if user.username else user_old.username
        user_old.first_name = user.first_name if user.first_name else user_old.first_name
        user_old.last_name = user.last_name if user.last_name else user_old.last_name
        user_old.email = user.email if user.email else user_old.email
        user_old.phone = user.phone if user.phone else user_old.phone

        session.add(user_old)
        session.commit()
        session.refresh(user_old)
    except:
        return JSONResponse(
            status_code=500,
            content=Error(code=500, message="unexpected error").json(),
        )



