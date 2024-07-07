from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    ValidationInfo,
    Field,
)
from typing import List
from datetime import datetime as dt

class CriminalPost(BaseModel):
    id: int
    title: str
    content: str
    tags: str | None
    created_at: dt | None
    modified_at: dt | None
    user_id: int

class CriminalReply(BaseModel):
    id: int
    content: str
    created_at: dt | None
    user_id: int

class CriminalStat(BaseModel):
    criminal_id: int
    num_reported: int

class CriminalInfo(BaseModel):
    id: int
    username: str
    is_blocked: bool | None

class CriminalResponse(BaseModel):
    criminal_stat: List[CriminalStat]
    criminal_info: List[CriminalInfo]

class Post(BaseModel):
    id: int
    title: str
    content: str

class Reply(BaseModel):
    id: int
    content: str

class AdminRecommend(BaseModel):
    post_id: int
    password: str

class AdminBlock(BaseModel):
    criminal_id: int
    password: str

class AdminReset(BaseModel):
    criminal_id: int
    password: str

class AdminDeletePost(BaseModel):
    post_id: int
    password: str

class AdminDeleteReply(BaseModel):
    reply_id: int
    password: str

class AdminDeleteAllPostReply(BaseModel):
    criminal_id: int
    password: str

class WikiWordResponse(BaseModel):
    id: int
    word: str
    yomikata: str
    category: str
    description: str
    link: str
    ready: bool

class WikiWordModify(BaseModel):
    id: int
    yomikata: str
    category: str
    description: str
    link: str
    ready: bool
    
    password: str

class StatNumUsersDaily(BaseModel):
    date: dt | None
    num_users: int | None