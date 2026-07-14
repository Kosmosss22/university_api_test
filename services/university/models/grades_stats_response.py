from pydantic import BaseModel


class GradesStatsResponse(BaseModel):
    count: int
    min: int
    max: int
    avg: float