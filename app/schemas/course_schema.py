from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    description: str
    length: int
    category: str

class CourseUpdate(BaseModel):
    title: str
    description: str
    length: int
    category: str