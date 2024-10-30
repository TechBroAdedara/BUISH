import logging
from fastapi import HTTPException
from sqlalchemy import desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import *
from sqlalchemy.orm import selectinload
from ..schemas.enrollment_schema import EnrollmentModel

from ..models import Enrollment, Progress, Course, User

class StudentService:
    async def enroll_for_course(self, user_id, course_id, session:AsyncSession):
        stmt = (select(Enrollment)
                .filter(
                        and_(
                            Enrollment.user_id == user_id,
                            Enrollment.course_id == course_id
                        )
                    )
                )
        existing_enrollment = (await session.execute(stmt)).scalar_one_or_none()

        if existing_enrollment:
            raise HTTPException(
                status_code=400,
                detail = "User has enrolled for this course"
            )
        try: 
            new_enrollment = Enrollment(
                user_id = user_id,
                course_id = course_id
            )

            session.add(new_enrollment)
            await session.commit()

            return {"message": f"Successfully enrolled for {new_enrollment.course_id}"}
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=500,
                detail = "Internal error. Contact admin"
            )
        
    async def get_enrolled_courses(self, user_id: int, session: AsyncSession):
        stmt = select(Enrollment, Course).join(Course).join(User).filter(User.id == user_id)  # Replace 1 with user_id
        enrolled_courses = await session.execute(stmt)
        result = enrolled_courses.scalars().all()
        return result