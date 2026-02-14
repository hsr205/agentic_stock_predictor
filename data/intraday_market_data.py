from config.config import settings
from alpha_vantage.timeseries import TimeSeries
from logger.logger import AppLogger

class IntraDayMarketData:

    def __init__(self) -> None:
        self.api_key:str = settings.alpha_vantage_api_key
        self._logger = AppLogger.get_logger(self.__class__.__name__)



    def get_market_data(self) -> None:
        time_series_data:TimeSeries = TimeSeries(key=self.api_key)
        data, meta = time_series_data.get_intraday('AAPL', interval='1min', outputsize='full')

        print(f"len(data) = {len(data)}")
        print(f"meta = {meta}")




