import asyncio
import queue
from collections import deque
from datetime import time
from pathlib import Path
from typing import Any

from alpaca.trading.client import TradingClient

from config.config import settings
from logger.logger import AppLogger
from trading_account.alpaca_trading_account import AlpacaTradingAccount
from utils.constants import Constants
from utils.trading_activity_csv_writer import TradingActivityCsvWriter

class AlpacaTradingEnvironmentProximalPolicyOptimization:
    alpaca_trading_account: AlpacaTradingAccount = AlpacaTradingAccount()

    def __init__(self) -> None:
        self._api_key_ppo: str = settings.api_key_ppo

        self._bar_queue: queue.Queue[dict] = queue.Queue()
        self._bar_history: deque[dict] = deque(maxlen=5000)
        self._latest_bar_dict: dict[str, Any] | None = None
        self._action_space: list[str] = Constants.ACTIONS_LIST
        self._first_bar_event: asyncio.Event = asyncio.Event()
        self._close_of_market_time: time = time(16, 0)
        self._api_secret_key_ppo: str = settings.api_secret_key_ppo
        self._trading_csv_writer: TradingActivityCsvWriter = TradingActivityCsvWriter(_base_dir=Path.cwd())
        self._trading_client: TradingClient = TradingClient(api_key=self._api_key_ppo,
                                                            secret_key=self._api_secret_key_ppo, paper=True)
        self.logger = AppLogger.get_logger(self.__class__.__name__)
