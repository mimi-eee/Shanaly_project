from pydantic import (
    BaseModel,
)
from typing import List
from datetime import datetime as dt

class UsersUsernameSearch(BaseModel):
    id: int

class PostUsernameSearch(BaseModel):
    id: int

class UsernameSearchResponse(BaseModel):
    id: int
    username: str
    status_msg: str
    posts: List[PostUsernameSearch]
    followers: List[UsersUsernameSearch]
    followees: List[UsersUsernameSearch]




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
