from yahooquery import Ticker
from retry import retry
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# ------- Yahoo Finance Data API -------- #
@retry(tries=10, delay=5)
def download_yahoo(*,
                   symbol: str | list,
                   kind: str="price",
                   period: str="5d",
                   timeframe: str="1d",
                   frequency: str="a") -> pd.DataFrame:
    ticker = (
        Ticker(
            symbol,
            asynchronous=True,
            progress=False,
            timeout=60,
            retry=3,
        )
    )
    if kind == "price":
        return (
            ticker
            .history(
                period=period,
                interval=timeframe,
                adj_timezone=True,
                adj_ohlc=False
            )
        )
    if kind == "financial_statement":
        return (
            ticker
            .all_financial_data(frequency=frequency)
        )