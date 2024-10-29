from pydantic import BaseModel


class UserCreateModel(BaseModel):
    username: str
    email: str
    password: str
    address: str
    role: str
    is_verified: bool = False

    class Config:
        from_attributes = True
