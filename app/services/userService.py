from fastapi import HTTPException
from ..schemas.user_schemas import UserCreateModel
from ..models import User

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import *


class UserService:
    #Create User Service
    async def create_user(self, user: UserCreateModel, session: AsyncSession):
        new_user = User(**user.model_dump())
        session.add(new_user)
        await session.commit()
        return new_user

    #Get all user service
    async def get_all_user(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))

        result = await session.execute(statement)

        users = result.all()
        
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

    async def get_user_by_email(self, email:str, session: AsyncSession):
        stmt = select(User).filter(User.email == email)
        result = await session.execute(stmt)

        user = result.scalar_one_or_none()
        return user
    
user_service = UserService()
