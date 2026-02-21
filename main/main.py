from logging import Logger

from data_extraction.alpaca_historic_data_extraction import AlpacaHistoricDataExtraction
from trading_account.alpaca_trading_account import AlpacaTradingAccount
from logger.logger import AppLogger
from alpaca.trading.enums import OrderSide

def main() -> int:
    logger: Logger = AppLogger().get_logger(__name__)

    try:
        alpaca_historic_data:AlpacaHistoricDataExtraction = AlpacaHistoricDataExtraction()
        alpaca_historic_data.export_historical_stock_data(year_of_data_to_collect=2025)

        # alpaca_trading_account: AlpacaTradingAccount = AlpacaTradingAccount()
        # # alpaca_trading_account.execute_action(ticker_str="AMZN",quantity=1,action_type=OrderSide.BUY)
        # # alpaca_trading_account.get_portfolio_positions_dict()
        # # alpaca_trading_account.get_account_data_dict()


    except Exception as e:
        logger.info(f"Exception Thrown: {e}")

    return 0


if __name__ == "__main__":
    main()
