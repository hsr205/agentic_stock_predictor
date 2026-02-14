import pandas as pd
import yfinance as yf

from config.config import settings
from logger.logger import AppLogger

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class IntraDayMarketData:

    def __init__(self) -> None:
        self._api_key: str = settings.api_key
        self.logger = AppLogger.get_logger(self.__class__.__name__)

    def get_market_data(self) -> None:
        dataframe: pd.DataFrame = yf.download("AAPL", start="2026-02-01", end="2026-02-08", interval="1m")

        self.logger.info(f"data.columns = {dataframe.columns}")
        print(dataframe.head())
