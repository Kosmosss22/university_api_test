from pydantic import BaseModel, Field

MIN_GRADE = 2
MAX_GRADE = 5


class GradesStatsResponse(BaseModel):
    count: int = Field(ge=0, description="Количество оценок (не может быть отрицательным)")
    min: int | None = Field(ge=MIN_GRADE, le=MAX_GRADE, description="Минимальная оценка")
    max: int | None = Field(ge=MIN_GRADE, le=MAX_GRADE, description="Максимальная оценка")
    avg: float | None = Field(ge=MIN_GRADE, le=MAX_GRADE, description="Средний балл")
