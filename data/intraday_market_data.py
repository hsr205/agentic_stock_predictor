import zlib

import pandas as pd
import yfinance as yf

from config.config import settings
from logger.logger import AppLogger
from utils.constants import Constants

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class IntraDayMarketData:

    def __init__(self) -> None:
        self._api_key: str = settings.api_key
        self.logger = AppLogger.get_logger(self.__class__.__name__)

    def get_market_data(self) -> None:
        dataframe: pd.DataFrame = yf.download("AAPL", start="2026-02-01", end="2026-02-08", interval="1m")

        self.logger.info(f"len(dataframe) = {len(dataframe):,}")
        self.logger.info(f"data.columns = {dataframe.columns}")
        print(dataframe.head())

    def _get_ticker_symbol_unique_label_dict(self) -> dict[str, int]:
        ticker_symbol_dict: dict[str, int] = {}
        ticker_symbol_list: list[str] = Constants.TICKER_SYMBOL_LIST

        for ticker_str in ticker_symbol_list:
            ticker_hash_value:int = zlib.adler32(ticker_str.encode('utf-8'))

            ticker_symbol_dict[ticker_str] = ticker_hash_value

        for key, value in ticker_symbol_dict.items():
            print(f"{key} -> {value}")

        return ticker_symbol_dict
