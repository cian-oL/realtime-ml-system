from loguru import logger

from src.kraken_api import KrakenMockAPI


def main() -> None:
    """
    Reads trades from Kraken API and pushes them to a topic.

    Args:
        None

    Returns:
        None

    """

    logger.info("Starting trades service")

    kraken_api = KrakenMockAPI(pair="BTC/USD")

    while True:
        trades = kraken_api.get_trades()

        for trade in trades:
            logger.info(f"Pushed trade to Kafka: {trade}")


if __name__ == "__main__":
    main()
