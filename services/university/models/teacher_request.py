from pydantic import BaseModel, ConfigDict

from services.university.models.subject_enum import SubjectEnum


class TeacherRequest(BaseModel):
    first_name: str
    last_name: str
    subject: SubjectEnum

    model_config = ConfigDict(use_enum_values=True)