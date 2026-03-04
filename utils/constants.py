from alpaca.trading.enums import OrderSide


class Constants:
    LOGGER_COLOR_RESET: str = "\033[0m"
    LOGGER_COLOR_WHITE: str = "\033[60m"
    LOGGER_COLOR_ORANGE: str = "\033[33m"
    LOGGER_COLOR_DARK_RED: str = "\033[31m"

    ALPACA_ACCOUNT_URL: str = "https://paper-api.alpaca.markets/v2/account"

    ORDER_SIDE_ACTIONS_LIST: list[OrderSide] = [OrderSide.BUY, OrderSide.SELL]
    ACTIONS_LIST: list[OrderSide | str] = [OrderSide.BUY, OrderSide.SELL, "HOLD"]

    TICKER_SYMBOL_TO_ID: dict[str, int] = {
        "AAPL": 1_001,
        "AMZN": 1_002,
        "GOOGL": 1_003,
        "META": 1_004,
        "MSFT": 1_005,
        "NVDA": 1_006,
        "TSLA": 1_007
    }

    TICKER_FEATURES_LIST: list[str] = [
        "portfolio_weight",
        "cost_basis_to_portfolio_value",
        "unrealized_pl_to_portfolio_value",
        "change_today"
    ]

    TICKER_SYMBOL_LIST: list[str] = ["AAPL", "AMZN", "GOOGL", "META", "MSFT", "NVDA", "TSLA"]
    CSV_OUTPUT_COLUMNS_LIST: list[str] = ["Timestep", "Timestamp", "Portfolio Equity", "Portfolio Cash Available"] + TICKER_SYMBOL_LIST
