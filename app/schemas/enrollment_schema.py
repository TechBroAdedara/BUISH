from pydantic import BaseModel

class EnrollmentModel(BaseModel):
    course_id: int
    user_id: int