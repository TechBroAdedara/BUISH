from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.enrollment_schema import EnrollmentModel

from ..services.studentService import StudentService

from .auth import get_student_user
from ..database.main import get_session

student_router = APIRouter(prefix="/user/student", tags=["Users/Student"])
student_user = Annotated[AsyncSession, Depends(get_student_user)]
Session = Annotated[dict, Depends(get_session)]
student_service = StudentService()


@student_router.post("/enroll/{course_id}")
async def enroll_for_course(course_id: int, session: Session, user: student_user):
    """ACCESS: STUDENT.
    Endpoint for enrolling a student in a course."""
    result = await student_service.enroll_for_course(
        user_id=user["id"], course_id=course_id, session=session
    )
    return result


@student_router.get("/enrollments")
async def get_enrolled_courses(session: Session, user: student_user):
    """ACCESS: STUDENT.
    Endpoint for getting a list of courses a student is enrolled in."""
    result = await student_service.get_enrolled_courses(user_id=user["id"], session=session)
    return {"Enrolled courses": result}
