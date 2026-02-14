from data.intraday_market_data import IntraDayMarketData
from logger.logger import AppLogger
from logging import Logger


def main() -> int:
    logger:Logger = AppLogger().get_logger(__name__)

    try:
        intraday_market_data: IntraDayMarketData = IntraDayMarketData()
        intraday_market_data.get_market_data()
    except Exception as e:
        logger.info(f"Exception Thrown: {e}")

    return 0


if __name__ == "__main__":
    main()
