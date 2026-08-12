from pydantic import BaseModel, ConfigDict


class SuccessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    detail: str
