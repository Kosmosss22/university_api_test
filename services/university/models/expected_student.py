from pydantic import BaseModel, ConfigDict
from services.university.models.base_student import DegreeEnum


class ExpectedStudent(BaseModel):
    first_name: str
    last_name: str
    email: str
    degree: DegreeEnum
    phone: str
    group_id: int

    model_config = ConfigDict(use_enum_values=True)