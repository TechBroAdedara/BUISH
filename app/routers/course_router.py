from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import get_current_user, get_student_user, get_teacher_user

from ..schemas.course_schema import CourseCreate, CourseUpdate
from ..database.main import get_session
from ..services.courseService import CourseService

course_router = APIRouter(prefix="/course", tags=["Courses"])
course_service = CourseService()

Session = Annotated[AsyncSession, Depends(get_session)]
general_user = Annotated[dict, Depends(get_current_user)]
student_user = Annotated[dict, Depends(get_student_user)]
teacher_user = Annotated[dict, Depends(get_teacher_user)]

@course_router.post("/create_course")
async def create_course(
                new_course: CourseCreate, 
                session: Session, 
                user: teacher_user
            ):
    """ACCESS: TEACHER.
    Endpoint for creating a new course"""
    result = await course_service.create_course(user["id"], new_course, session)
    return result


@course_router.get("/{id}")
async def get_course(id, session:Session, _:general_user):
    """ACCESS: TEACHER.
    Endpoint for getting a specific course"""
    result = await course_service.get_course(id, session)
    return {"course":result}


@course_router.get("/all")
async def get_all_courses(session: Session):
    return await course_service.get_all_courses(session)

@course_router.get("/all/{category}")
async def get_course_by_category(category, session: Session, _:general_user):
    """ACCESS: GENERAL.
    Endpoint for getting all courses for a given category"""
    result = await course_service.get_courses_by_category(category, session)
    return {f"{category} courses": result}

@course_router.get("/contents/{course_id}")
async def get_course_content(course_id:int, session: Session, _:general_user):
    result = await course_service.get_course_content(course_id=course_id, session=session)
    return {"content": result}