from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import get_admin_user
from ..database.main import get_session
from ..services.adminService import AdminService

admin_user = Annotated[dict, Depends(get_admin_user)]
admin_router = APIRouter(prefix="/users/admin", tags=["Users/Admin"])
user_service = AdminService()
Session = Annotated[AsyncSession, Depends(get_session)]


@admin_router.get("/{id}")
async def get_user(id, session: Session, _: admin_user):
    """ACCESS: ADMIN.
    Gets details of a user by id"""
    result = await user_service.get_user(id, session)
    return {"user": result}


@admin_router.get("/")
async def get_all_users(session: Session, _: admin_user):
    """ACCESS: ADMIN.
    Gets details of all users"""
    result = await user_service.get_all_users(session)
    return {"users":result}

@admin_router.get("/courses/all/{id}")
async def get_user_created_courses(id:int, session: Session, user: admin_user):
    """ACCESS: ADMIN.
    Gets courses created by a specific user"""
    result = await user_service.get_user_created_courses(id, session)
    return {f"courses created by {user['username']}" : result}
