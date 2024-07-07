from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
)
from fastapi.responses import (
    JSONResponse,
)
from domain.data.data_schema import (
    ErrorResponse,
    PriceGetYahoo,
    PriceGetYahooMultiple,
    FinancialStatementGetYahoo,
    PriceResponseYahoo,
)
from domain.data.data_helper import download_yahoo

import pandas as pd
import warnings
warnings.filterwarnings("ignore")

router = APIRouter(prefix="/api/data", tags=["Data API"])

@router.get("/price_yahoo",
            response_model=List[PriceResponseYahoo],
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_price_yahoo(*, symbol: str, period: str="5d", timeframe: str="1d"):

    def exception_process(df):
        try:
            df = df.assign(time=lambda df_: pd.to_datetime(df_["date"]).astype("int64") / 10**9) # Unix Time
        except:
            df = (
                df
                .assign(time=lambda df_: df_["date"].astype(str).str[0:10])
                .assign(time=lambda df_: pd.to_datetime(df_["time"]).astype("int64") / 10**9) # Unix Time
            )
        return df

    input_ = PriceGetYahoo(
        symbol=symbol,
        period=period,
        timeframe=timeframe,
    )

    data = download_yahoo(
        kind="price",
        symbol=input_.symbol,
        period=input_.period,
        timeframe=input_.timeframe,
    )  

    if len(data) == 0:
        raise HTTPException(status_code=400, detail="No data")

    data = (
        data
        .reset_index()
        .pipe(exception_process)
        .loc[:,["symbol","time","open","high","low","close","volume"]] # for Tradingview
        .to_dict(orient="records")
    )

    return data

@router.post("/price_yahoo_multiple",
            # response_model=List[PriceResponseYahoo],
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_price_yahoo_multiple(*, symbol: PriceGetYahooMultiple):

    def add_int_order(df):
        df["date"] = pd.Series([1,2] * df["symbol"].nunique())
        return df

    data = download_yahoo(
        symbol=symbol.symbol,
        kind="price",
        period="7d",
        timeframe="1d"
    )
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="No data")
    data = (
        data
        .loc[:,["close"]]
        .reset_index()
        .assign(date=lambda df_: df_["date"].astype(str).str[0:10])
        .assign(date=lambda df_: pd.to_datetime(df_["date"]))
        .sort_values(["symbol","date"], ascending=True)
        
    )
    df_price = (
        data
        .loc[:,["symbol","close"]]
        .groupby("symbol")
        .tail(1)
        .set_index("symbol")
    )
    df_ret = (
        data
        .groupby("symbol")
        .tail(2)
        .reset_index(drop=True)
        .pipe(add_int_order)
        .pivot(index="symbol", columns="date", values="close")
        .set_axis(["t-1","t"], axis="columns")
        .assign(sim_ret_pct=lambda df_: df_["t"].div(df_["t-1"]).sub(1).mul(100).round(2))
        .loc[:,["sim_ret_pct"]]
    )
    data = (
        df_price
        .join(df_ret)
        .to_dict("index")
    )
    return data

@router.get("/financial_statement_yahoo",
            responses={
                400: {"model": ErrorResponse, "description": "Error Response"},
            })
def get_financial_statement_yahoo(*, symbol: str, frequency: str="a"):

    input_ = FinancialStatementGetYahoo(
        symbol=symbol,
        frequency=frequency,
    )

    data = download_yahoo(
        kind="financial_statement",
        symbol=input_.symbol,
        frequency=input_.frequency, 
    )

    if not isinstance(data, pd.DataFrame):
        raise HTTPException(status_code=400, detail="データがありません。")

    if len(data) == 0:
        raise HTTPException(status_code=400, detail="データがありません。")

    data = (
        data
        .reset_index()
        .assign(asOfDate=lambda df_: df_["asOfDate"].astype(str).str[0:10])
        .fillna('')
        .to_dict(orient="records")
    )
    
    return data