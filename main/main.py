import asyncio
from logging import Logger

from data_extraction.alpaca_historic_data_extraction import AlpacaHistoricDataExtraction
from logger.logger import AppLogger


async def main() -> int:
    logger: Logger = AppLogger().get_logger(__name__)

    try:

        list_of_years_to_collect: list[int] = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

        alpaca_historic_data_extraction: AlpacaHistoricDataExtraction = AlpacaHistoricDataExtraction()

        alpaca_historic_data_extraction.export_historical_stock_data(
            list_of_years_to_collect=list_of_years_to_collect)

        # alpaca_trading_env_random_policy: AlpacaTradingEnvironmentRandomPolicy = AlpacaTradingEnvironmentRandomPolicy()
        #
        # await alpaca_trading_env_random_policy.initialize_trading_environment_random_policy()

        # alpaca_trading_env_ppo: AlpacaTradingEnvironmentPPO = AlpacaTradingEnvironmentPPO()
        #
        # await alpaca_trading_env_ppo.step(tensordict=TensorDict())

        # ppo_config: PPOConfig = PPOConfig()
        # environment = AlpacaTradingEnvironmentPPO(config=ppo_config)
        # alpaca_trading_ppo_neural_network: AlpacaTradingPPONeuralNetwork = AlpacaTradingPPONeuralNetwork(
        #     env=environment, config=ppo_config)
        #
        # alpaca_trading_ppo_neural_network.train_model()


    except Exception as e:
        logger.info(f"Exception Thrown: {e}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
