from typing import List, Annotated
from fastapi import (
    APIRouter,
    Depends,
    Path,
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
    PostDraft,
)
from domain.account.account_router import get_current_user
from domain.draft.draft_schema import (
    PostSave,
    PostSaveResponse,
)
from database import get_session
from datetime import datetime as dt

router = APIRouter(prefix="/api/draft", tags=["Draft API"])

@router.post("/save")
def save_draft_report(*,
                      session: Session=Depends(get_session),
                      current_user: Users=Depends(get_current_user),
                      post_save: PostSave):
    # Check whether the number of drafts are over 3
    drafts = (
        session
        .exec(
            select(PostDraft)
            .where(PostDraft.user_id == current_user.id)
        )
        .all()
    )
    if len(drafts) > 2:
        raise HTTPException(status_code=400, detail="Over 3 drafts are not allowed")
    
    # Add a draft to database
    draft = PostDraft(
        user_id=current_user.id,
        username=current_user.username,

        title=post_save.title,
        content=post_save.content,
        tags=post_save.tags,
        data=post_save.data,

        created_at=dt.now(),
    )
    session.add(draft)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "Created successfully"}
    )

@router.get("/list",
            response_model=List[PostSaveResponse])
def get_draft_list(*,
                   session: Session=Depends(get_session),
                   current_user: Users=Depends(get_current_user)):
    drafts = (
        session
        .exec(
            select(PostDraft)
            .where(PostDraft.user_id == current_user.id)
        )
        .all()
    )
    if len(drafts) == 0:
        raise HTTPException(status_code=400, detail="No data")
    return drafts

@router.delete("/delete/{draft_id}")
def delete_draft_report(*,
                   session: Session=Depends(get_session),
                   current_user: Users=Depends(get_current_user),
                   draft_id: int=Path(gt=0)):
    draft = (
        session
        .exec(
            select(PostDraft)
            .where(
                (PostDraft.id == draft_id) &
                (PostDraft.user_id == current_user.id)
            )
        )
        .first()
    )
    if draft is None:
        raise HTTPException(status_code=400, detail="No data")
    session.delete(draft)
    session.commit()
    return JSONResponse(
        status_code=200,
        content={"detail": "Deleted successfully"}
    )