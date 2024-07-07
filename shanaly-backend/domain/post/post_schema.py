from typing import List
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

class UserLike(BaseModel):
    id: int
    username: str

class UserRepost(BaseModel):
    id: int
    username: str

class Reply(BaseModel):
    id: int
    
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    report: bool
    tags: str | None
    created_at: dt
    modified_at: dt | None
    detail_id: int | None
    user: User | None
    replies: List[Reply] | None
    like_users: List[UserLike] | None
    repost_users: List[UserRepost] | None

class DetailResponse(BaseModel):
    data: dict

class PostCreate(BaseModel):
    title: str = Field(max_length=50)
    content: str = Field(max_length=500)
    report: bool
    tags: str | None = Field(default=None)
    detail: dict | None = Field(default=None)

    @field_validator("title", "content")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="空白はできません。")
        return v
    
    @field_validator("detail")
    @classmethod
    def not_empty(cls, v: dict) -> dict:
        if v == {}:
            raise HTTPException(status_code=400, detail="Blank dictionary is not allowed")
        return v
    
class PostModify(BaseModel):
    post_id: int
    title: str = Field(max_length=50)
    content: str = Field(max_length=500)
    tags: str | None

    @field_validator("title", "content")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="Blank value is not allowed")
        return v
    
class PostLike(BaseModel):
    post_id: int

class PostRepost(BaseModel):
    post_id: int