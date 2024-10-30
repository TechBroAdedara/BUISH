from datetime import timedelta
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.main import get_session
from ..models.user import User
from ..schemas.user_schemas import UserCreateModel
from ..services.userService import UserService
from ..schemas.token_schema import TokenSchema
from ..utils.access_tokens import create_access_token, decode_token

#---------------------------Dependencies------------------------
session = Annotated[AsyncSession, Depends(get_session)]
user_service = UserService()
auth_router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#---------------------------Security------------------------
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")
password_request_form = Annotated[OAuth2PasswordRequestForm, Depends()]

#---------------------------Routes------------------------
@auth_router.post("/create_user")
async def create_user(new_user: UserCreateModel, session: session):
    hashed_password = bcrypt_context.hash(new_user.password)

    existing_user = await user_service.get_user_by_email(new_user.email, session)
    print(existing_user)
    if existing_user:
        raise HTTPException(
            status_code= 400,
            detail= "User already exists"
        )
    try:
        user = User(
            username = new_user.username,
            email = new_user.email,
            address = new_user.address,
            role = new_user.role,
            password_hash = hashed_password
        )

        session.add(user)
        await session.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500, 
            detail= "Internal error"
        )
    
    
@auth_router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: password_request_form, session: session):
    #Check if user exists in database
    existing_user = await user_service.get_user_by_email(form_data.username, session)   
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    #User exists, so verify stored password with entered password
    if not bcrypt_context.verify(form_data.password, existing_user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )
    
    token = create_access_token(
        id=existing_user.id,
        email= existing_user.email,
        username= existing_user.username,
        role = existing_user.role,
        is_verified= existing_user.is_verified,
        expires_delta=timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token:str = Depends(oauth2_bearer)):
    return decode_token(token)