from fastapi import HTTPException
from pydantic import EmailStr
from datetime import timedelta, datetime
from jose import JWTError, jwt
from ..config import Config


def create_access_token(
    email: EmailStr,
    username: str,
    role: str,
    is_verified,
    expires_delta: timedelta,
):
    data_to_encode = {
        "sub": email,
        "username": username,
        "role": role,
        "verification_status": is_verified,
    }
    
    expires = datetime.utcnow() + expires_delta
    data_to_encode.update({"exp": expires})
    return jwt.encode(data_to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email = payload.get("sub")
        username = payload.get("username")
        role = payload.get("role")
        verification_status = payload.get("verification_status")

        if not all([email, username, role]):
            raise HTTPException(
                status_code=401,
                detail="Could not validate user",
            )

        return {
            "email": email,
            "username": username,
            "role": role,
            "verification_status": verification_status,
        }
    except JWTError as j:
        print(j)
        raise HTTPException(
            status_code=401,
            detail="Could not validate user.",
        )
