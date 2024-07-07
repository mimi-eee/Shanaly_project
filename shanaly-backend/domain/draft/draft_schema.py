from typing import List
from pydantic import (
    BaseModel,
    field_validator,
    Field,
)
from fastapi import HTTPException
from datetime import datetime as dt

class PostSave(BaseModel):
    title: str = Field(max_length=50)
    content: str = Field(max_length=500)
    tags: dict = Field(default={})
    data: dict = Field(default={})

    @field_validator("title", "content")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="Blank value is not allowed")
        return v

class PostSaveResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: dict
    data: dict