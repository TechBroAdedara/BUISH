from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.main import get_session
from app.routers.auth import get_teacher_user
from app.services.adminService import AdminService
from app.services.courseService import CourseService

teacher_router = APIRouter(
    prefix= "/user/teacher",
    tags = ["User/Teacher"]
    )

Session = Annotated[AsyncSession, Depends(get_session)]
teacher_user = Annotated[dict, Depends(get_teacher_user)]

@teacher_router.get("/courses/my_courses")
async def get_my_courses(session: Session, user: teacher_user):
    """ACCESS: TEACHER.
    Gets courses created by teacher"""
    user_service = AdminService()
    result = await user_service.get_user_created_courses(user["email"], session)
    return {f"courses created by {user['username']}" : result}