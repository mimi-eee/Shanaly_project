from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import (
    JSONResponse,
)
from sqlmodel import (
    Session,
    select,
)
from models import (
    Users,
    UsersUsersFollowLink,
    Post,
    UsersPostLikeLink,
)
from domain.account.account_router import get_current_user
from domain.user.user_schema import (
    UserInfoResponse,
)
from database import get_session
import pandas as pd

router = APIRouter(prefix="/api/user", tags=["User API"])

@router.get("/info/{username}",
            response_model=UserInfoResponse,
            )
def get_info_user(*,
                  session: Session=Depends(get_session),
                  username: str):
    # User data
    user = (
        session
        .exec(
            select(Users)
            .where(Users.username == username)
        )
        .first()
    )
    # Number of Likes the user has received
    posts = (
        session
        .exec(
            select(Post.id, UsersPostLikeLink.user_id)
            .join(UsersPostLikeLink)
            .where(Post.user_id == user.id)
        )
        .all()
    )
    if len(posts) == 0:
        total_num_likes = 0
    else:     
        total_num_likes = pd.DataFrame(posts)["user_id"].count()
    return {
        "total_num_likes": int(total_num_likes),
        "user_info": user,
    }

@router.post("/follow/{username}")
def follow_user(*,
                session: Session=Depends(get_session),
                current_user: Users=Depends(get_current_user),
                username: str):
    # Get the target user ID with username
    target_user = (
        session
        .exec(
            select(Users)
            .where(Users.username == username)
        )
        .first()
    )
    if target_user is None:
        raise HTTPException(status_code=400, detail="No data")
    # Check whether already followed the target user or not
    followed_or_not = (
        session
        .exec(
            select(UsersUsersFollowLink)
            .where(
                (UsersUsersFollowLink.follower_id == current_user.id) &
                (UsersUsersFollowLink.followee_id == target_user.id)
            )
        )
        .first()
    )
    # If the current user is not following the target user,
    # Then let the current user follows the target user
    if followed_or_not is None:

        # Current User
        user = (
            session
            .exec(
                select(Users)
                .where(Users.id == current_user.id)
            )
            .first()
        )

        user.followees.append(target_user)
        session.add(user)
        session.commit()
        return JSONResponse(
            status_code=200,
            content={"detail": "Follow"}
        )
    
    # If the current user already followed the target user,
    # Then let the current user UN-follow the target user
    else:
        session.delete(followed_or_not)
        session.commit()
        return JSONResponse(
            status_code=200,
            content={"detail": "Unfollow"}
        )
    
@router.post("/report/{criminal_id}")
def report_criminal(*,
                session: Session=Depends(get_session),
                current_user: Users=Depends(get_current_user),
                criminal_id: int):
    # Prevent self-report
    if current_user.id == criminal_id:
        raise HTTPException(status_code=400, detail="No Self Report")
    # Get the info of potential criminal
    criminal = session.get(Users, criminal_id)
    if criminal is None:
        raise HTTPException(status_code=400, detail="No data")

    try:
        criminal.reporters.append(current_user)
        session.add(criminal)
        session.commit()
        return JSONResponse(
            status_code=200,
            content={"detail": "ユーザー申告完了"}
        )
    except:
        raise HTTPException(status_code=400, detail="もう申告したユーザーです。")
    