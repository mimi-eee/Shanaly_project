from pydantic import (
    BaseModel,
)
from typing import List
from datetime import datetime as dt

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

class Post(BaseModel):
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

class Follower(BaseModel):
    id: int
    username: str
    status_msg: str

class Followee(BaseModel):
    id: int
    username: str
    status_msg: str

class Plan(BaseModel):
    id: int
    plan_name_jpn: str
    plan_name_eng: str

class UserInfo(BaseModel):
    id: int
    username: str
    status_msg: str
    picture: str | None
    plan: Plan
    posts: List[Post]
    repost_posts: List[Post]
    like_posts: List[Post]
    followers: List[Follower]
    followees: List[Followee]

class UserInfoResponse(BaseModel):
    total_num_likes: int
    user_info: UserInfo