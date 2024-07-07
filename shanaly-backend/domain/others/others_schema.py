from pydantic import (
    BaseModel,
    field_validator,
)
from fastapi import HTTPException

class SuccessResponse(BaseModel):
    detail: str

class ErrorResponse(BaseModel):
    detail: str

class WikiWordGet(BaseModel):
    keyword: str
    
    @field_validator("keyword")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="Blank value is not allowed")
        return v

class WikiWordResponse(BaseModel):
    word: str
    description: str
    link: str
    ready: bool

class SymbolDictionaryResponse(BaseModel):
    symbol: str 
    name: str
    asset_type: str