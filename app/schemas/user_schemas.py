from pydantic import BaseModel


class UserCreateModel(BaseModel):
    username: str
    email: str
    password: str
    address: str
    role: str

    class Config:
        from_attributes = True
