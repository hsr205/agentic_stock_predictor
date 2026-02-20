import calendar
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.models.bars import BarSet
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from tqdm import tqdm

from config.config import settings
from logger.logger import AppLogger
from utils.constants import Constants

pd.set_option('display.max_columns', None)

class AlpacaHistoricDataExtraction:

    def __init__(self) -> None:
        self._api_key: str = settings.api_key
        self._api_secret_key: str = settings.api_secret_key
        self._stock_historical_data_client: StockHistoricalDataClient = StockHistoricalDataClient(self._api_key,
                                                                                                  self._api_secret_key)
        self.logger = AppLogger.get_logger(self.__class__.__name__)

    def export_historical_stock_data(self) -> None:
        try:
            year_num: int = 2025

            eastern_timezone: ZoneInfo = ZoneInfo("America/New_York")

            for ticker_symbol in tqdm(Constants.TICKER_SYMBOL_LIST, desc="Extracting Historical Stock Data"):

                file_name_str: str = ""
                dataframe_list: list[pd.DataFrame] = []

                for month_num in tqdm(range(1, 13), desc="Extracting Specific Stock Data"):

                    days_in_month_num: int = self.get_days_in_month(year=year_num, month=month_num)

                    start_datetime: datetime = datetime(
                        year=year_num,
                        month=month_num,
                        day=1,
                        hour=0,
                        minute=0,
                        second=0,
                        tzinfo=eastern_timezone
                    )

                    end_datetime: datetime = datetime(
                        year=year_num,
                        month=month_num,
                        day=days_in_month_num,
                        hour=23,
                        minute=59,
                        second=59,
                        tzinfo=eastern_timezone
                    )

                    stock_bars_request: StockBarsRequest = StockBarsRequest(
                        timeframe=TimeFrame.Minute,
                        symbol_or_symbols=ticker_symbol,
                        start=start_datetime,
                        end=end_datetime
                    )

                    bars_set: BarSet = self._stock_historical_data_client.get_stock_bars(stock_bars_request)
                    df: pd.DataFrame = bars_set.df.reset_index()[
                        ["symbol", "timestamp", "open", "close", "high", "low", "volume"]]

                    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                    df["timestamp"] = df["timestamp"].dt.tz_convert("America/New_York")

                    df = df.set_index("timestamp")

                    df = df.between_time("09:30", "16:00")

                    df = df.reset_index()

                    dataframe_list.append(df)

                    file_name_str = self.get_file_name_str(ticker_symbol=ticker_symbol)

                result_dataframe:pd.DataFrame = pd.concat(dataframe_list)

                export_file_path: Path = Path(f"historical_stock_data/{file_name_str}")

                self.logger.info(f"\nExporting data to: {export_file_path}")

                result_dataframe.to_csv(path_or_buf=export_file_path)

                self.logger.info(f"\nSuccessfully exported data to: {export_file_path}")

        except Exception as e:
            self.logger.error(f"Exception Thrown: {e}")

    def get_file_name_str(self, ticker_symbol: str) -> str:
        start_datetime_str: str = "2025" + "_" + "01" + "_" + "01"
        end_datetime_str: str = "2025" + "_" + "12" + "_" + "31"

        return ticker_symbol + "_" + start_datetime_str + "_" + end_datetime_str + ".csv"

    def get_days_in_month(self, year, month):
        num_days_int: int = calendar.monthrange(year, month)[1]
        return num_days_int
