from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlmodel import (
    Session,
    select,
    col,
    func,
    desc,
)
from models import (
    Users,
    Post,
    UsersPostLikeLink,
)
from domain.search.search_schema import (
    UsernameSearchResponse,
    PostResponse,
)
from database import get_session
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

router = APIRouter(prefix="/api/search", tags=["Search API"])

@router.get("/user/{username}",
            response_model=List[UsernameSearchResponse])
def search_user_by_username(*,
                            session: Session=Depends(get_session),
                            skip: int=0,
                            limit: int=10, # PARAMETER
                            username: str):
    users = (
        session
        .exec(
            select(Users)
            .where(
                (col(Users.username).ilike(f"%{username}%")) &
                (Users.id != 1) # Do not expose Admin user in search result
            )
            .order_by(Users.username.asc())
            .offset(skip)
            .limit(limit)
        )
        .all()
    )
    if len(users) == 0:
        raise HTTPException(status_code=400, detail="No data")
    return users

@router.get("/tag/latest/{tag}",
            response_model=List[PostResponse])
def search_post_by_tag_latest(*,
                              session: Session=Depends(get_session),
                              skip: int=0,
                              limit: int=10, # PARAMETER
                              tag: str):
    posts = (
        session
        .exec(
            select(Post)
            .where(
                col(Post.tags).ilike(f"%{tag}%")
            )
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        .all()
    )
    if len(posts) == 0:
        raise HTTPException(status_code=400, detail="No data")
    return posts

@router.get("/tag/popular/{tag}",
            response_model=List[PostResponse]
            )
def search_post_by_tag_popular(*,
                               session: Session=Depends(get_session),
                               tag: str):
    # [PARAMETER]
    N_DAYS = 30
    N_POST_PER_REQUEST = 20
    
    # Define period
    today_datetime = dt.now().date()
    past_datetime = today_datetime - timedelta(days=N_DAYS)

    # Find Posts with a specific tag within a recent period
    posts_id = (
        session
        .exec(
            select(Post.id)
            .where(
                (Post.created_at >= past_datetime) &
                (col(Post.tags).ilike(f"%{tag}%"))
            )
        )
        .all()
    )
    if len(posts_id) == 0:
        raise HTTPException(status_code=400, detail="No data")
    
    # Select Popular Top 100 posts
    popular_posts = (
        session
        .exec(
            select(
                UsersPostLikeLink.post_id,
                func.count(UsersPostLikeLink.user_id).label("likes"),
            )
            .where(
                col(UsersPostLikeLink.post_id).in_(posts_id)
            )
            .group_by(UsersPostLikeLink.post_id)
            .order_by(desc("likes"))
            .limit(100)
        )
        .fetchall()
    )
    if len(popular_posts) == 0:
        raise HTTPException(status_code=400, detail="No data")
    if len(popular_posts) < N_POST_PER_REQUEST:
        N_POST_PER_REQUEST = len(popular_posts)
    
    # Among the 100 popular posts's post IDs
    # Pick N posts randomly
    randomly_selected_post_id_lst = (
        pd
        .DataFrame(popular_posts)
        ["post_id"]
        .sample(
            n=N_POST_PER_REQUEST,
            replace=False
        )
        .to_list()
    )
    # Return those random popular posts to the user
    # With full post information
    posts = (
        session
        .exec(
            select(Post)
            .where(
                col(Post.id).in_(randomly_selected_post_id_lst)
            )
            # .order_by(Post.created_at.desc())
        )
        .all()
    )
    if len(posts) == 0:
        raise HTTPException(status_code=400, detail="No data")
    return posts