from pydantic import BaseModel


class DeleteResponse(BaseModel):
    success: bool
    detail: str  