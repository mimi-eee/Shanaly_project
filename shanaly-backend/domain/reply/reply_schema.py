from pydantic import (
    BaseModel,
    field_validator,
    Field,
)

from fastapi import HTTPException
from datetime import datetime as dt

class SuccessResponse(BaseModel):
    detail: str

class ErrorResponse(BaseModel):
    detail: str

class User(BaseModel):
    id: int
    username: str
    picture: str | None

class ReplyResponse(BaseModel):
    id: int
    content: str
    created_at: dt
    user: User

class ReplyCreate(BaseModel):
    post_id: int
    content: str = Field(max_length=200)

    @field_validator("content")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="Blank value is not allowed")
        return v

class ReplyModify(BaseModel):
    reply_id: int
    content: str = Field(max_length=200)

    @field_validator("content")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="Blank value is not allowed")
        return v