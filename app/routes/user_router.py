from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..routes.auth import get_current_user
from ..database.main import get_session
from ..services.userService import UserService

general_user = Annotated[dict, Depends(get_current_user)]
user_router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()
session = Annotated[AsyncSession, Depends(get_session)]


@user_router.get("/{id}")
async def get_user(id, session: session, _: general_user):
    result = await user_service.get_user(id, session)
    return {"user": result}


@user_router.get("/")
async def get_all_users(session: session, _: general_user):
    result = await user_service.get_all_users(session)
    return {"users":result}

@user_router.get("/courses/course")
async def get_user_created_courses(session: session, user: general_user):
    result = await user_service.get_user_created_courses(user["id"], session)
    return {f"courses created by {user["username"]}" : result}
