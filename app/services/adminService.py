from fastapi import HTTPException
from ..schemas.user_schemas import UserCreateModel
from ..models import User

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import *
from sqlalchemy.orm import selectinload


class AdminService:    
    #Used for the auth router
    async def get_user_by_email(self, email:str, session: AsyncSession):
        stmt = select(User).filter(User.email == email)
        result = await session.execute(stmt)

        user = result.scalar_one_or_none()
        return user
    
    #Get all user service
    async def get_all_users(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))

        results = await session.execute(statement)

        users = results.scalars().all()
        
        return users

    #Get specific user service
    async def get_user(self, id: int, session: AsyncSession):
        stmt = select(User).filter(User.id == id)
        result = await session.execute(stmt)

        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code= 404,
                detail="User Not Found"
            )
        return user


    async def get_user_created_courses(self, email:str, session: AsyncSession):
        stmt = select(User).options(selectinload(User.created_courses)).filter(User.email == email)
        result = await session.execute(stmt)

        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User Not Found"
            )
        
        courses = user.created_courses 

        return courses

user_service = AdminService()
