from pydantic import BaseModel


class DeleteSuccessResponse(BaseModel):
    detail: str


class DeleteErrorResponse(BaseModel):
    detail: str
