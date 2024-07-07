from typing import List
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
    col,
    func,
    desc,
    delete,
    SQLModel,
)
from sqlalchemy import delete
from models import (
    Users,
    UsersUsersReportLink,
    Reply,
    Post,
    UsersPostLikeLink,
    Wiki,
)
from domain.admin.admin_schema import (
    AdminRecommend,
    AdminBlock,
    AdminReset,
    AdminDeletePost,
    AdminDeleteReply,
    AdminDeleteAllPostReply,
    CriminalResponse,
    CriminalPost,
    CriminalReply,
    CriminalInfo,
    WikiWordResponse,
    WikiWordModify,
    StatNumUsersDaily,
)
from passlib.context import CryptContext
import os
from database import get_session
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

# PARAMETERS: Get Environment Variables
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

router = APIRouter(prefix="/api/admin", tags=["Admin API"])

def sqlmodel_to_df(objects: List[SQLModel], set_index: bool = True) -> pd.DataFrame:
    """Converts SQLModel objects into a Pandas DataFrame.
    Usage
    ----------
    df = sqlmodel_to_df(list_of_sqlmodels)
    Parameters
    ----------
    :param objects: List[SQLModel]: List of SQLModel objects to be converted.
    :param set_index: bool: Sets the first column, usually the primary key, to dataframe index."""

    records = [obj.model_dump() for obj in objects]
    columns = list(objects[0].model_json_schema()["properties"].keys())
    df = pd.DataFrame.from_records(records, columns=columns)
    return df

@router.get("/list/potential_criminals",
            response_model=CriminalResponse
            )
def get_potential_criminals(*, session: Session=Depends(get_session)):
    # [PARAMETER]
    N_DAYS = 30
    
    # Define period
    today_datetime = dt.now().date()
    past_datetime = today_datetime - timedelta(days=N_DAYS)
    
    # Get criminal statistics
    criminal_stat = (
        session
        .exec(
            select(
                UsersUsersReportLink.criminal_id,
                func.count(UsersUsersReportLink.reporter_id).label("num_reported"),
            )
            .where(
                (UsersUsersReportLink.created_at >= past_datetime)
            )
            .group_by(UsersUsersReportLink.criminal_id)
            .order_by(desc("num_reported"))
        )
        .mappings().all()
    )

    if len(criminal_stat) == 0:
        raise HTTPException(status_code=400, detail="申告されたユーザーがありません。")

    criminals_id_lst = pd.DataFrame(criminal_stat)["criminal_id"].to_list()

    # Get criminals info
    criminals = (
        session
        .exec(
            select(Users)
            .where(
                col(Users.id).in_(criminals_id_lst)
            )
        )
        .all()
    )

    return {
        "criminal_stat": criminal_stat,
        "criminal_info": criminals,
    }

@router.get("/list/criminal_post",
            response_model=List[CriminalPost])
def get_criminal_post(*, session: Session=Depends(get_session), user_id: int):
    # Get User's Post
    posts = (
        session
        .exec(
            select(Post)
            .where(Post.user_id == user_id)
        )
        .all()
    )
    if len(posts) == 0:
        raise HTTPException(status_code=400, detail="データがありません。")
    return posts

@router.get("/list/criminal_reply",
            response_model=List[CriminalReply])
def get_criminal_reply(*, session: Session=Depends(get_session), user_id: int):
    # Get User's Reply
    replies = (
        session
        .exec(
            select(Reply)
            .where(Reply.user_id == user_id)
        )
        .all()
    )
    if len(replies) == 0:
        raise HTTPException(status_code=400, detail="データがありません。")
    return replies


@router.patch("/block",
             response_model=CriminalInfo)
def block_criminal(*,
               session: Session=Depends(get_session),
               block_input: AdminBlock):
    # Check the admin password
    if block_input.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")

    target_criminal = session.get(Users, block_input.criminal_id)
    target_criminal.is_blocked = True
    session.add(target_criminal)
    session.commit()
    session.refresh(target_criminal)
    return target_criminal

@router.patch("/unblock",
             response_model=CriminalInfo)
def unblock_criminal(*,
                 session: Session=Depends(get_session),
                 block_input: AdminBlock):
    # Check the admin password
    if block_input.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")

    target_criminal = session.get(Users, block_input.criminal_id)
    target_criminal.is_blocked = False
    session.add(target_criminal)
    session.commit()
    session.refresh(target_criminal)
    return target_criminal

@router.patch("/reset")
def reset_criminal_reported(*,
               session: Session=Depends(get_session),
               reset_input: AdminReset):
    # Check the admin password
    if reset_input.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")
    (
        session
        .exec(
            delete(UsersUsersReportLink)
            .where(UsersUsersReportLink.criminal_id == reset_input.criminal_id)
        )
    )
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": f"ユーザーID = {reset_input.criminal_id}, 申告数のがリセットされました。"}
    )

@router.delete("/post")
def delete_post(*,
               session: Session=Depends(get_session),
               delete_input: AdminDeletePost):
    # Check the admin password
    if delete_input.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")
    
    # Get the post
    post = (
        session
        .exec(
            select(Post)
            .where(Post.id == delete_input.post_id)
        )
        .first()
    )

    if post is None:
        raise HTTPException(status_code=400, detail="データがありません。")

    session.delete(post)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "投稿の削除完了"}
    )

@router.delete("/reply")
def delete_reply(*,
               session: Session=Depends(get_session),
               delete_input: AdminDeleteReply):
    # Check the admin password
    if delete_input.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")
    
    # Get the reply
    reply = (
        session
        .exec(
            select(Reply)
            .where(Reply.id == delete_input.reply_id)
        )
        .first()
    )

    if reply is None:
        raise HTTPException(status_code=400, detail="データがありません。")

    session.delete(reply)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "返信の削除完了"}
    )

@router.delete("/user_posts")
def delete_criminal_posts(*,
               session: Session=Depends(get_session),
               delete_input: AdminDeleteAllPostReply):
    # Check the admin password
    if delete_input.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")
    # Get this criminal's posts
    user = (
        session
        .exec(
            select(Users)
            .where(Users.id == delete_input.criminal_id)
        )
        .first()
    )

    if len(user.posts) == 0:
        raise HTTPException(status_code=400, detail="データがありません。")

    # And delete each post by looping
    for post in user.posts:
        session.delete(post)
        session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "すべての投稿の削除完了"}
    )

@router.delete("/user_replies")
def delete_criminal_replies(*,
               session: Session=Depends(get_session),
               delete_input: AdminDeleteAllPostReply):
    # Check the admin password
    if delete_input.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")
    (
        session
        .exec(
            delete(Reply)
            .where(Reply.user_id == delete_input.criminal_id)
        )
    )
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "すべての返信の削除完了"}
    )

@router.post("/recommend")
def recommend_post(*,
                   session: Session=Depends(get_session),
                   admin_recommend: AdminRecommend):
    # Check the admin password
    if admin_recommend.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")
    
    # Check whether already recommended or not
    recommended_post = (
        session
        .exec(
            select(UsersPostLikeLink)
            .where(
                (UsersPostLikeLink.post_id == admin_recommend.post_id)
            )
        )
        .first()
    )

    # If the admin already recommended the target post before, then reverse it
    if recommended_post is not None:
        session.delete(recommended_post)
        session.commit()
        return JSONResponse(
            status_code=200,
            content={"detail": f"投稿ID = {admin_recommend.post_id}, おすすめ解除"}
        )
    # Otherwise, just recommend the target post
    else:
        post = session.get(Post, admin_recommend.post_id)
        if post is None:
            raise HTTPException(status_code=400, detail="データがありません。")
        
        # Get admin user
        admin = session.get(Users, 1)
        # Add the admin to like_users in the post
        post.like_users.append(admin)

        session.add(post)
        session.commit() 
        return JSONResponse(
            status_code=200,
            content={"detail": f"投稿ID = {admin_recommend.post_id}, おすすめ完了"}
        )

@router.get("/wiki_get/",
            response_model=WikiWordResponse)
def get_wiki_word(*,
                  session: Session=Depends(get_session),
                  word: str):
    word = (
        session.
        exec(
            select(Wiki)
            .where(Wiki.word == word)
        )
        .first()
    )
    if word is None:
        raise HTTPException(status_code=400, detail="No data")
    return word

@router.patch("/wiki_modify")
def modify_wiki_word(*,
                     session: Session=Depends(get_session),
                     word_modify: WikiWordModify):
    # Check the admin password
    if word_modify.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="パスワードが間違いです。")
    
    word = session.get(Wiki, word_modify.id)
    input_dict = word_modify.model_dump(exclude_unset=True)
    word.sqlmodel_update(input_dict)

    session.add(word)
    session.commit()
    return {"detail": "用語の修正が変更されました"}

@router.get("/stat/num_users_daily", response_model=List[StatNumUsersDaily])
def get_stat_num_users_daily(*,
                  session: Session=Depends(get_session)):
    # Exclude some users from stats
    exclude_email_lst = [
        "admin@shanaly.com",
        "ayoanenim122137zz@gmail.com",
        "shanaly_info@shanaly.net",
        "vancluse1@gmail.com",
    ]

    # Get data from Users table
    users = (
        session
        .exec(
            select(Users)
            .where(
                col(Users.email).not_in(exclude_email_lst)
            )
        )
        .all()
    )
    # Compute the daily number of users
    data = (
        sqlmodel_to_df(users)
        .loc[:, ["id","created_at"]]
        .rename(columns={"created_at":"date"})
        .groupby(pd.Grouper(key="date", freq="D"))
        .count()
        .reset_index()
        .rename(columns={"id":"num_users"})
        .to_dict(orient="records")
    )
    return data