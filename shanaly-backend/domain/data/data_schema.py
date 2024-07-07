from pydantic import (
    BaseModel,
    field_validator,
)
from typing import List
from fastapi import HTTPException

class SuccessResponse(BaseModel):
    detail: str

class ErrorResponse(BaseModel):
    detail: str

# Yahoo Finance
class PriceGetYahoo(BaseModel):
    symbol: str
    period: str
    timeframe: str
    
    @field_validator("symbol")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="Blank value is not allowed")
        return v
    
class PriceGetYahooMultiple(BaseModel):
    symbol: List[str]

    @field_validator("symbol")
    @classmethod
    def not_empty_list(cls, v: list) -> list:
        if len(v) == 0 :
            raise HTTPException(status_code=400, detail="Empty list is not allowed")
        return v

    @field_validator("symbol")
    @classmethod
    def no_more_than(cls, v: list) -> list:
        if len(v) > 6 :
            raise HTTPException(status_code=400, detail="No more than 6 symbols")
        return v
    
class FinancialStatementGetYahoo(BaseModel):
    symbol: str
    frequency: str
    
    @field_validator("symbol", "frequency")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise HTTPException(status_code=400, detail="Blank value is not allowed")
        return v
    
class PriceResponseYahoo(BaseModel):
    symbol: str
    time: int # Unix Time
    open: float
    high: float
    low: float
    close: float
    volume: float | None

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

class SymbolIndexYahooResponse(BaseModel):
    symbol: str 
    name_jpn: str | None
    name_eng: str | None
    kind_jpn: str | None
    kind_eng: str | None
    period_jpn: str | None
    period_eng: str | None
    timeframe_jpn: str | None
    timeframe_eng: str | None
    kind_arg: str | None
    period_arg: str | None
    timeframe_arg: str | None