from typing import List
from fastapi import (
    APIRouter,
    Depends,
    Path,
    HTTPException,
)
from fastapi.responses import (
    Response,
    JSONResponse,
)
from sqlmodel import (
    Session,
)
from models import (
    Post,
    Reply,
    Users,
)
from domain.user.user_router import get_current_user
from domain.reply.reply_schema import (
    SuccessResponse,
    ErrorResponse,
    ReplyResponse,
    ReplyCreate,
    ReplyModify,
)
from database import get_session
from datetime import datetime as dt

router = APIRouter(prefix="/api/reply", tags=["Reply API"])

@router.get("/all/{post_id}",
            response_model=List[ReplyResponse],
            responses={
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_all_replies(*, session: Session=Depends(get_session), post_id: int=Path(gt=0)):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")
    replies = post.replies
    replies = replies[::-1]
    return replies

@router.post("/create",
             response_model=ReplyResponse,
             responses={
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def create_reply(*,
                 session:
                 Session=Depends(get_session),
                 current_user: Users=Depends(get_current_user),
                 reply_create: ReplyCreate):
    # [Checking Blocked user]
    # If this user is blocked by admin, then do not allow the user to write something
    # Instead, send a message
    if current_user.is_blocked == True:
        raise HTTPException(
            status_code=400,
            detail="当該アカウントはShanalyの定める運営ルールに違反している可能性があるため、一時的にブロックされました。詳細はHPのお問い合わせからご照会ください。",
            headers={"WWW-Authenticate": "Bearer"}
        )

    post = session.get(Post, reply_create.post_id)
    if post is None:
        raise HTTPException(status_code=400, detail="No data")
    reply = Reply(
        content=reply_create.content,
        post=post,
        created_at=dt.now(),
        user=current_user,
    )
    session.add(reply)
    session.commit()
    session.refresh(reply)
    return reply

@router.patch("/modify",
              response_model=ReplyResponse,
              responses={
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def modify_reply(*,
                 session: Session=Depends(get_session),
                 current_user: Users=Depends(get_current_user),
                 reply_modify: ReplyModify):
    reply = session.get(Reply, reply_modify.reply_id)
    if reply is None:
        raise HTTPException(status_code=400, detail="No data")
    if current_user.id != reply.user_id:
        raise HTTPException(status_code=400, detail="No permission")
    input_dict = reply_modify.model_dump(exclude_unset=True)
    reply.sqlmodel_update(input_dict)

    session.add(reply)
    session.commit()
    session.refresh(reply)

    return reply

@router.delete("/delete/{reply_id}",
              responses={
                 200: {"model": SuccessResponse, "description": "Success Response"},
                 400: {"model": ErrorResponse, "description": "Error Response"},
            })
def delete_reply(*,
                 session: Session=Depends(get_session),
                 current_user: Users=Depends(get_current_user),
                 reply_id: int=Path(gt=0)):
    reply = session.get(Reply, reply_id)
    if reply is None:
        raise HTTPException(status_code=400, detail="No data")
    if current_user.id != reply.user_id:
        raise HTTPException(status_code=400, detail="No permission")
    session.delete(reply)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "Deleted successfully"}
    )