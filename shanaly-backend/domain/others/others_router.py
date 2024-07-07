from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlmodel import (
    Session,
    select,
)
from models import (
    Wiki,
    SymbolDictionary,
)
from domain.others.others_schema import (
    ErrorResponse,
    WikiWordGet,
    WikiWordResponse,
    SymbolDictionaryResponse,
)
from database import get_session

router = APIRouter(prefix="/api/others", tags=["Others API"])

@router.get("/wiki/dict",
            response_model=List[str],
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_wiki_dict(*, session: Session=Depends(get_session)):
    data = (
        session
        .exec(
            select(Wiki.word)
        )
        .all()
    )
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="No data")
    
    return data

@router.get("/wiki/word",
            response_model=WikiWordResponse,
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_wiki_word(*, session: Session=Depends(get_session), keyword: str):
    input_ = WikiWordGet(keyword=keyword)
    data = (
        session
        .exec(
            select(Wiki)
            .where(Wiki.word == input_.keyword)
        )
        .one()
    )
    if data is None:
        raise HTTPException(status_code=400, detail="No data")
    return data

@router.get("/symbol/dictionary",
            response_model=List[SymbolDictionaryResponse],
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_symbol_dictionary(*, session: Session=Depends(get_session)):
    data = (
        session
        .exec(
            select(SymbolDictionary)
        )
        .all()
    )
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="No data")
    
    return data