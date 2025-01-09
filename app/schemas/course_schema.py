from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    title: str
    description: str
    length: int
    category: str
    image_url: Optional[str]

class CourseUpdate(BaseModel):
    title: str
    description: str
    length: int
    category: str