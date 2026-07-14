from pydantic import BaseModel
from services.university.models.subject_enum import SubjectEnum


class TeacherRequest(BaseModel):
    first_name: str
    last_name: str
    subject: SubjectEnum

    class Config:
        use_enum_values = True