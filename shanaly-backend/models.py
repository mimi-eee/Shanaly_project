from typing import Optional, List
from sqlmodel import Field, SQLModel, Column, DateTime, Relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime as dt

# Like Table: Users & Post
class UsersPostLikeLink(SQLModel, table=True):

    __tablename__ = "users_post_like_link"

    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    post_id: int | None = Field(default=None, foreign_key="post.id",primary_key=True)
    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

# Like Table: Users & Reply
class UsersReplyLikeLink(SQLModel, table=True):

    __tablename__ = "users_reply_like_link"

    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    reply_id: int | None = Field(default=None, foreign_key="reply.id", primary_key=True)
    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

# Repost Table: Users & Post
class UsersPostRepostLink(SQLModel, table=True):

    __tablename__ = "users_post_repost_link"

    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    post_id: int | None = Field(default=None, foreign_key="post.id",primary_key=True)
    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

# Follow Table: Users & Users
class UsersUsersFollowLink(SQLModel, table=True):

    __tablename__ = "users_users_follow_link"

    follower_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    followee_id: int | None = Field(default=None, foreign_key="users.id",primary_key=True)

    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

# Report Table: Users & Users
class UsersUsersReportLink(SQLModel, table=True):

    __tablename__ = "users_users_report_link"

    reporter_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    criminal_id: int | None = Field(default=None, foreign_key="users.id",primary_key=True)

    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

# Users Table
# [!] PostgresSQL does not allow to create a table named 'user' because it is reserved one
class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    email: str = Field(nullable=False, unique=True, max_length=100)
    username: str = Field(nullable=False, unique=True, max_length=30)
    password: str = Field(nullable=False, min_length=3)
    status_msg: str = Field(nullable=True, default="こんにちは", max_length=200)
    picture: str = Field(nullable=True)

    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    login_at: dt = Field(sa_column=Column(DateTime(timezone=True), nullable=True), default=None)

    is_verified: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    is_blocked: bool = Field(default=False, nullable=True)

    # with Post
    posts: List["Post"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all,delete",
            "order_by": "desc(Post.created_at)",
        },
    )

    # with Reply
    replies: List["Reply"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all,delete"},
    )

    # with UsersPostLikeLink
    like_posts: List["Post"] = Relationship(
        back_populates="like_users",
        link_model=UsersPostLikeLink,
        sa_relationship_kwargs={
            "order_by": "desc(Post.created_at)",
        },
    )

    # with UsersReplyLikeLink
    like_replies: List["Reply"] = Relationship(
        back_populates="like_users",
        link_model=UsersReplyLikeLink,
    )

    # with UsersPostRepostLink
    repost_posts: List["Post"] = Relationship(
        back_populates="repost_users",
        link_model=UsersPostRepostLink,
        sa_relationship_kwargs={
            "order_by": "desc(Post.created_at)"
        },
    )

    # UsersUsersFollowLink: Followers
    followers: List["Users"] = Relationship(
        back_populates="followees",
        link_model=UsersUsersFollowLink,
        sa_relationship_kwargs={
            "primaryjoin": "Users.id==UsersUsersFollowLink.followee_id",
            "secondaryjoin": "Users.id==UsersUsersFollowLink.follower_id",
        },
    )
    
    # UsersUsersFollowLink: Followees
    followees: List["Users"] = Relationship(
        back_populates="followers",
        link_model=UsersUsersFollowLink,
        sa_relationship_kwargs={
            "primaryjoin": "Users.id==UsersUsersFollowLink.follower_id",
            "secondaryjoin": "Users.id==UsersUsersFollowLink.followee_id",
        },
    )

    # UsersUsersReportLink: Reporters
    reporters: List["Users"] = Relationship(
        back_populates="criminals",
        link_model=UsersUsersReportLink,
        sa_relationship_kwargs={
            "primaryjoin": "Users.id==UsersUsersReportLink.criminal_id",
            "secondaryjoin": "Users.id==UsersUsersReportLink.reporter_id",
        },
    )

    # UsersUsersReportLink: Criminals
    criminals: List["Users"] = Relationship(
        back_populates="reporters",
        link_model=UsersUsersReportLink,
        sa_relationship_kwargs={
            "primaryjoin": "Users.id==UsersUsersReportLink.reporter_id",
            "secondaryjoin": "Users.id==UsersUsersReportLink.criminal_id",
        },
    )

    # with Plan
    plan_id: int = Field(default=None, nullable=False, foreign_key="plan.id")
    plan: Optional["Plan"] = Relationship(back_populates="users")

# Post Table
class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(max_length=50)
    content: str = Field(max_length=500)
    report: bool = Field(nullable=False)
    tags: str = Field(nullable=True)
    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    modified_at: dt = Field(sa_column=Column(DateTime(timezone=True), nullable=True), default=None)

    # with Detail
    detail_id: int = Field(default=None, nullable=True, foreign_key="detail.id")
    detail: Optional["Detail"] = Relationship(
        back_populates="post",
        sa_relationship_kwargs={"cascade": "all,delete"},
    )

    # with Reply
    replies: List["Reply"] = Relationship(
        back_populates="post",
        sa_relationship_kwargs={"cascade": "all,delete"},
    )

    # with Users
    user_id: int = Field(default=None, nullable=True, foreign_key="users.id")
    user: Users = Relationship(back_populates="posts")

    # with UsersPostLikeLink
    like_users: List["Users"] = Relationship(
        back_populates="like_posts",
        link_model=UsersPostLikeLink,
    )

    # with UsersPostRepostLink
    repost_users: List["Users"] = Relationship(
        back_populates="repost_posts",
        link_model=UsersPostRepostLink,
    )

# Reply Table
class Reply(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    content: str = Field(max_length=100)
    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), nullable=False))

    # with Post
    post_id: int = Field(default=None, nullable=True, foreign_key="post.id")
    post: Post = Relationship(back_populates="replies")

    # with Users
    user_id: int = Field(default=None, nullable=True, foreign_key="users.id")
    user: Users = Relationship(back_populates="replies")

    # with UsersReplyLikeLink
    like_users: List["Users"] = Relationship(
        back_populates="like_replies",
        link_model=UsersReplyLikeLink,
    )

# Detail Table
class Detail(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: dict = Field(sa_column=Column(JSONB))

    # with Post
    post: Post = Relationship(back_populates="detail")

# Post Save Table
class PostDraft(SQLModel, table=True):

    __tablename__ = "post_draft"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(index=True)
    username: str = Field(index=True)

    title: str = Field(max_length=50)
    content: str = Field(max_length=500)
    tags: dict = Field(sa_column=Column(JSONB))
    data: dict = Field(sa_column=Column(JSONB))
    
    created_at: dt = Field(sa_column=Column(DateTime(timezone=True), nullable=False))

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_name_jpn: str = Field(nullable=False, max_length=20)
    plan_name_eng: str = Field(nullable=False, max_length=20)

    users: List["Users"] = Relationship(back_populates="plan")

# Wiki Table
class Wiki(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    word: str = Field(nullable=False, index=True)
    category: str = Field(nullable=True, index=True)
    yomikata: str = Field(nullable=True)
    description: str = Field(nullable=False)
    link: str = Field(nullable=True)
    ready: bool = Field(nullable=True)

# Symbol Dictionary Table
class SymbolDictionary(SQLModel, table=True):

    __tablename__ = "symbol_dictionary"

    id: int | None = Field(default=None, primary_key=True)

    symbol: str = Field(nullable=False)
    name: str = Field(nullable=True)
    market: str = Field(nullable=True)
    asset_type: str = Field(nullable=True)
    country: str = Field(nullable=True)