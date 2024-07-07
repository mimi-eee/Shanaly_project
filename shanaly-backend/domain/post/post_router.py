from typing import List
from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    HTTPException,
)
from fastapi.responses import (
    Response,
    JSONResponse,
)
from sqlmodel import (
    Session,
    select,
    col,
    func,
    desc,
)
from models import (
    Post,
    Detail,
    Users,
    UsersPostLikeLink,
    UsersPostRepostLink,
    UsersUsersFollowLink,
)
from domain.account.account_router import get_current_user
from domain.post.post_schema import (
    SuccessResponse,
    ErrorResponse,
    PostResponse,
    DetailResponse,
    PostCreate,
    PostModify,
    PostLike,
    PostRepost,
)
from database import get_session
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

router = APIRouter(prefix="/api/post", tags=["Post API"])

@router.get("/popular_posts", response_model=List[PostResponse])
def get_popular_posts(*,
                     session: Session=Depends(get_session)):
    # [PARAMETER]
    N_DAYS = 30
    N_POST_PER_REQUEST = 20
    
    # Define period
    today_datetime = dt.now().date()
    past_datetime = today_datetime - timedelta(days=N_DAYS)

    # Group By post_id
    # Count(user_id) As "num_likes"
    # During the last 30 days
    # Limit by 100
    popular_posts = (
        session
        .exec(
            select(
                UsersPostLikeLink.post_id,
                func.count(UsersPostLikeLink.user_id).label("likes"))
            .where(
                (UsersPostLikeLink.created_at >= past_datetime)
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

    # Among the 100 popular posts, pick N posts randomly
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

@router.get("/latest_posts", response_model=List[PostResponse])
def get_latest_posts(*,
                     session: Session=Depends(get_session),
                     limit: int=10, # PARAMETER
                     last_post_id:int=Query(default=None, ge=1)):
    if last_post_id is None:
        posts = (
            session
            .exec(
                select(Post)
                .order_by(Post.created_at.desc())
                .limit(limit)
            )
            .all()
        )
    else:
        posts = (
            session
            .exec(
                select(Post)
                .where(Post.id < last_post_id)
                .order_by(Post.created_at.desc())
                .limit(limit)
            )
            .all()
        )
    if len(posts) == 0:
        raise HTTPException(status_code=400, detail="No data")
    return posts

@router.get("/following_posts", response_model=List[PostResponse])
def get_following_posts(*,
                        session: Session=Depends(get_session),
                        current_user: Users=Depends(get_current_user),
                        limit: int=10, # PARAMETER
                        last_post_id:int=Query(default=None, ge=1)):
    followees_id_lst = (
        session
        .exec(
            select(UsersUsersFollowLink.followee_id)
            .where(UsersUsersFollowLink.follower_id == current_user.id)
        )
        .all()
    )
    if last_post_id is None:
        posts = (
            session
            .exec(
                select(Post)
                .where(
                    col(Post.user_id).in_(followees_id_lst)
                )
                .order_by(Post.created_at.desc())
                .limit(limit)
            )
            .all()
        )
    else:
        posts = (
            session
            .exec(
                select(Post)
                .where(
                    col(Post.user_id).in_(followees_id_lst) &
                    (Post.id < last_post_id)
                )
                .order_by(Post.created_at.desc())
                .limit(limit)
            )
            .all()
        )
    if len(posts) == 0:
        raise HTTPException(status_code=400, detail="No data")
    return posts

@router.get("/recommended_posts",
            response_model=List[PostResponse])
def get_recommended_posts(*,
                        session: Session=Depends(get_session),
                        limit: int=10, # PARAMETER
                        last_post_id:int=Query(default=None, ge=1)):
    # Get post IDs recommend by Admin
    post_ids = (
        session
        .exec(
            select(UsersPostLikeLink.post_id)
            .where(UsersPostLikeLink.user_id == 1)
        )
        .all()
    )

    if len(post_ids) == 0:
        raise HTTPException(status_code=400, detail="No Data")

    if last_post_id is None:
        posts = (
            session
            .exec(
                select(Post)
                .where(
                    col(Post.id).in_(post_ids)
                )
                .order_by(Post.created_at.desc())
                .limit(limit)
            )
            .all()
        )
    else:
        posts = (
            session
            .exec(
                select(Post)
                .where(
                    col(Post.id).in_(post_ids) &
                    (Post.id < last_post_id)
                )
                .order_by(Post.created_at.desc())
                .limit(limit)
            )
            .all()
        )
    if len(posts) == 0:
        raise HTTPException(status_code=400, detail="No Data")
    return posts

@router.get("/one/{post_id}",
            response_model=PostResponse,
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_a_specific_post(*, session: Session=Depends(get_session), post_id: int=Path(gt=0)):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")
    return post

@router.get("/detail/{post_id}", 
            response_model=DetailResponse,
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_detail(*, session: Session=Depends(get_session), post_id: int=Path(gt=0)):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")
    detail = post.detail
    if detail is None:
        raise HTTPException(status_code=400, detail="No data")
    return detail

@router.post("/create",
             responses={
                 200: {"model": SuccessResponse, "description": "Success Response"},
                 400: {"model": ErrorResponse, "description": "Error Response"},
             })
def create_post(*,
                session: Session=Depends(get_session),
                current_user: Users=Depends(get_current_user),
                post_create: PostCreate):
    
    # [Checking Blocked user]
    # If this user is blocked by admin, then do not allow the user to write something
    # Instead, send a message
    if current_user.is_blocked == True:
        raise HTTPException(
            status_code=400,
            detail="当該アカウントはShanalyの定める運営ルールに違反している可能性があるため、一時的にブロックされました。詳細はHPのお問い合わせからご照会ください。",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Simple Post Case
    if post_create.detail is None:
        post = Post(
            title=post_create.title,
            content=post_create.content,
            report=post_create.report,
            tags=post_create.tags,
            created_at=dt.now(),
            user=current_user,
        )
    # Report Case
    else:
        detail = Detail(data=post_create.detail)
        post = Post(
            title=post_create.title,
            content=post_create.content,
            report=post_create.report,
            tags=post_create.tags,
            created_at=dt.now(),
            detail=detail,
            user=current_user,
        )
    session.add(post)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "Created successfully"}
    )

@router.patch("/modify",
              response_model=PostResponse,
              responses={
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def modify_post(*,
                session: Session=Depends(get_session),
                current_user: Users=Depends(get_current_user),
                post_modify: PostModify):
    post = session.get(Post, post_modify.post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="No permission")

    input_dict = post_modify.model_dump(exclude_unset=True)
    post.sqlmodel_update(input_dict)
    post.modified_at = dt.now()

    session.add(post)
    session.commit()
    session.refresh(post)

    return post

@router.delete("/delete/{post_id}",
              responses={
                 200: {"model": SuccessResponse, "description": "Success Response"},
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def delete_post(*,
                session: Session=Depends(get_session),
                current_user: Users=Depends(get_current_user),
                post_id: int=Path(gt=0)):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="No permission")
    
    session.delete(post)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "Deleted successfully"}
    )

@router.post("/like",
             responses={
                 200: {"model": SuccessResponse, "description": "Success Response"},
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def like_post(*,
              session: Session=Depends(get_session),
              current_user: Users=Depends(get_current_user),
              post_like: PostLike):
    post = session.get(Post, post_like.post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")
    try:
        post.like_users.append(current_user)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post
    except:
        raise HTTPException(status_code=400, detail="Already Liked it")
    
@router.post("/repost",
             responses={
                 200: {"model": SuccessResponse, "description": "Success Response"},
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def repost_post(*,
              session: Session=Depends(get_session),
              current_user: Users=Depends(get_current_user),
              post_repost: PostRepost):
    post = session.get(Post, post_repost.post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")
    
    # Check whether already reposted or not
    reposted_post = (
        session
        .exec(
            select(UsersPostRepostLink)
            .where(
                (UsersPostRepostLink.user_id == current_user.id) &
                (UsersPostRepostLink.post_id == post_repost.post_id)
            )
        )
        .first()
    )
    # If a user already reposted the target post before, then reverse it
    if reposted_post is not None:
        session.delete(reposted_post)
        session.commit()
        return JSONResponse(
            status_code=200,
            content={"detail": "Unrepost"}
        )
    # Otherwise, just repost the target post
    else:
        post.repost_users.append(current_user)
        session.add(post)
        session.commit()
        # session.refresh(post)
        # return post
        return JSONResponse(
            status_code=200,
            content={"detail": "Repost"}
        )