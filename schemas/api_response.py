from pydantic import BaseModel


class ApiResponse(BaseModel):
    error: bool
    message: str
