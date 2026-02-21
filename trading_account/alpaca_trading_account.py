from typing import Any

import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.models import Order
from alpaca.trading.requests import MarketOrderRequest
from requests.models import Response

from config.config import settings
from logger.logger import AppLogger
from utils.constants import Constants


class AlpacaTradingAccount:

    def __init__(self) -> None:
        self._api_key: str = settings.api_key
        self._api_secret_key: str = settings.api_secret_key
        self._trading_client: TradingClient = TradingClient(self._api_key, self._api_secret_key, paper=True)
        self.logger = AppLogger.get_logger(self.__class__.__name__)

    def execute_action(self, ticker_str: str, quantity: int, action_type: OrderSide) -> None:

        try:

            market_order_request: MarketOrderRequest = MarketOrderRequest(
                symbol=ticker_str,
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

    def get_portfolio_positions_dict(self) -> list[dict[str, Any]]:
        portfolio_list: list = self._trading_client.get_all_positions()

        portfolio_positions_list: list[dict[str, Any]] = []

        for position in portfolio_list:
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

            portfolio_positions_list.append(ticker_data_dict)

        return portfolio_positions_list

    def get_account_data_dict(self) -> dict[str, float]:
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
