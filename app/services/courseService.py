from fastapi import HTTPException

from ..models.content import Content
from ..models.course import Course

from ..schemas.course_schema import CourseCreate, CourseUpdate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import *

class CourseService:
    async def get_course(self, course_id:int, session: AsyncSession):
        stmt = select(Course).filter(Course.id == course_id)
        result = await session.execute(stmt)
        course = result.scalar_one_or_none()

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        return course
    

    async def create_course(self, user_id:int , course:CourseCreate, session: AsyncSession):
        
        stmt = select(Course).filter(Course.title == course.title)
        result = await session.execute(stmt)
        course_exists = result.scalar_one_or_none()

        if course_exists:
            raise HTTPException(
                status_code=400,
                detail =" Course already exists"
            )
        
        new_course = Course(
            title=course.title,
            description=course.description,
            length=course.length,
            category= course.category
        )
        new_course.created_by = user_id

        session.add(new_course)
        await session.commit()

        return {"message": "Course created successfully",
                "course": new_course}

    async def update_course(self, course_id: int, course: CourseUpdate, session: AsyncSession):
        pass

    async def delete_course(self, course_id: int, session: AsyncSession):
        pass

    async def get_courses_by_category(self, category: str, session: AsyncSession):
        stmt = select(Course).filter(Course.category == category)
        result = await session.execute(stmt)
        courses = result.scalars().all()

        return courses

    async def get_course_content(self, course_id: int, session: AsyncSession):
        stmt = select(Content).filter(Content.course_id== course_id)
        course_content = (
            await session.execute(stmt)
            ).scalars().all()
        

        return course_content