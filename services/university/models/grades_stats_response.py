from pydantic import BaseModel, field_validator
from typing import Optional


class GradesStatsResponse(BaseModel):
    count: int
    min: Optional[int] = None
    max: Optional[int] = None
    avg: Optional[float] = None

    @field_validator('count')
    @classmethod
    def count_must_be_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError('count must be non-negative')
        return v

    @field_validator('min', 'max')
    @classmethod
    def grade_must_be_valid(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 2 or v > 5):
            raise ValueError('Grade must be between 2 and 5')
        return v

    @field_validator('avg')
    @classmethod
    def avg_must_be_valid(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < 2.0 or v > 5.0):
            raise ValueError('Average grade must be between 2.0 and 5.0')
        return v