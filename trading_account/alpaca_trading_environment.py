import random
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar

import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.models import Order
from alpaca.trading.requests import MarketOrderRequest
from requests.models import Response
from torch import Tensor

from config.config import settings
from logger.logger import AppLogger
from trading_account.historical_stock_data_obj import HistoricalStockDataObj
from utils.constants import Constants


class AlpacaTradingEnvironment:
    ObsType: TypeVar = TypeVar("ObsType")

    def __init__(self, ticker_symbol_str: str) -> None:
        self._api_key: str = settings.api_key
        self._ticker_symbol_str: str = ticker_symbol_str
        self._api_secret_key: str = settings.api_secret_key
        self._trading_client: TradingClient = TradingClient(self._api_key, self._api_secret_key, paper=True)
        self._action_space: list[str] = Constants.ACTIONS_LIST
        self.logger = AppLogger.get_logger(self.__class__.__name__)

    def execute_action(self, quantity: int, action_type: OrderSide) -> None:

        try:

            market_order_request: MarketOrderRequest = MarketOrderRequest(
                symbol=self._ticker_symbol_str,
                qty=quantity,
                side=action_type,
                order_type=OrderType.MARKET,
                time_in_force=TimeInForce.DAY
            )

            market_order: Order = self._trading_client.submit_order(
                order_data=market_order_request
            )

            self.logger.info(
                f"Successful {market_order.side.name} {market_order.qty} share(s) of {market_order.symbol}")

        except Exception as e:
            self.logger.warning(f"Exception Thrown: {e}")

    def _get_ticker_data_dict(self) -> dict[str, Any]:
        portfolio_list: list = self._trading_client.get_all_positions()

        for position in portfolio_list:

            if position.symbol == self._ticker_symbol_str:
                ticker_data_dict: dict[str, Any] = {
                    "ticker_symbol": position.symbol,
                    "quantity": position.qty,
                    "qty_available": position.qty_available,
                    "exchange_name": position.exchange.name,
                    "cost_basis": position.cost_basis,
                    "market_value": position.market_value,
                    "current_price": position.current_price,
                    "change_today": position.change_today,
                    "unrealized_intraday_pl": position.unrealized_intraday_pl,
                    "unrealized_intraday_plpc": position.unrealized_intraday_plpc
                }

                return ticker_data_dict

    def _get_account_data_dict(self) -> dict[str, float]:
        try:

            headers_dict: dict[str, str] = {
                "accept": "application/json",
                "APCA-API-KEY-ID": self._api_key,
                "APCA-API-SECRET-KEY": self._api_secret_key
            }

            response: Response = requests.get(Constants.ALPACA_ACCOUNT_URL, headers=headers_dict)
            response_dict: dict[str, Any] = response.json()

            cash_float: float = float(response_dict["cash"])
            equity_float: float = float(response_dict["equity"])
            last_equity_float: float = float(response_dict["last_equity"])
            buying_power_float: float = float(response_dict["buying_power"])
            portfolio_value_float: float = float(response_dict["portfolio_value"])
            effective_buying_power_float: float = float(response_dict["effective_buying_power"])

            account_data_dict: dict[str, float] = {
                "cash": cash_float,
                "equity": equity_float,
                "last_equity": last_equity_float,
                "buying_power": buying_power_float,
                "portfolio_value": portfolio_value_float,
                "effective_buying_power": effective_buying_power_float,
            }

            return account_data_dict


        except Exception as e:
            self.logger.error(f"Exception thrown: {e}")

    def step(self, action_str: str) -> tuple[ObsType, Tensor, bool, bool, dict[str, Any]]:
        pass

        # return observation, reward_tensor, terminated, truncated, _

    def get_ticker_state_dict(self) -> dict[str, Any]:

        account_data_dict: dict[str, Any] = self._get_account_data_dict()
        ticker_data_dict: dict[str, Any] = self._get_ticker_data_dict()
        ticker_state_dict: dict[str, Any] = account_data_dict | ticker_data_dict

        return ticker_state_dict

    def retrieve_individual_stock_data_list(self) -> list[HistoricalStockDataObj]:

        file_path: Path = self._get_data_file_path()

        historical_stock_data_list: list[HistoricalStockDataObj] = []

        with open(file=file_path, mode="r") as data_file:

            next(data_file)

            for observation_str in data_file:

                observation_str = observation_str.strip()

                if not observation_str:
                    continue

                values: list[str] = observation_str.split(",")

                historical_stock_obj: HistoricalStockDataObj = HistoricalStockDataObj(
                    observation_num=int(values[0]),
                    ticker_symbol_str=values[1],
                    ticker_symbol_id=int(values[2]),
                    timestamp=datetime.fromisoformat(values[3]),
                    open=float(values[4]),
                    close=float(values[5]),
                    high=float(values[6]),
                    low=float(values[7]),
                    volume=float(values[8])
                )

                historical_stock_data_list.append(historical_stock_obj)

        for index, historical_data_obj in enumerate(historical_stock_data_list):
            self.logger.info(f"historical_data_obj = {historical_data_obj}")

        return historical_stock_data_list

    def _get_data_file_path(self) -> Path:

        data_directory_path: Path = Path("historical_stock_data/")

        file_path: Path = Path()

        for element in data_directory_path.iterdir():
            if element.is_file() and self._ticker_symbol_str in str(element):
                file_path = element
                break

        return file_path

    def get_random_action_from_action_space(self) -> str:
        return random.choice(self._action_space)
