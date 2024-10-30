from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..routes.auth import get_current_user

from..schemas.course_schema import CourseCreate, CourseUpdate
from ..database.main import get_session
from ..models import Course
from ..services.courseService import CourseService

course_router = APIRouter(prefix="/course", tags=["Courses"])
course_service = CourseService()
session = Annotated[AsyncSession, Depends(get_session)]
general_user = Annotated[dict, Depends(get_current_user)]


@course_router.post("/create_course")
async def create_course(
                new_course: CourseCreate, 
                session: session, 
                user: general_user
            ):
    """Endpoint for creating a new course"""
    result = await course_service.create_course(user["id"], new_course, session)
    return result


@course_router.get("/{id}")
async def get_course(id, session:session, _:general_user):
    """Endpoint for getting a specific course"""
    result = await course_service.get_course(id, session)
    return result



@course_router.get("/all/{category}")
async def get_course_by_category(category, session: session, _:general_user):
    """ Endpoint for getting all courses for a given category"""
    result = await course_service.get_courses_by_category(category, session)
    return result