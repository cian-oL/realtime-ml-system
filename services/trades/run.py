from typing import Union
from loguru import logger
from quixstreams import Application

from kraken_api.mock import KrakenMockApi
from kraken_api.websocket import KrakenWebsocketApi


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: Union[KrakenWebsocketApi, KrakenMockApi],
):
    """
    Reads trades from Kraken API and pushes them to a topic.

    Args:
        kafka_broker_address: str
        kafka_topic: str
        kraken_api: Union[KrakenWebsocketApi, KrakenMockApi]

    Returns:
        None

    """

    logger.info("Starting trades service")

    # initialise quixstreams application
    app = Application(broker_address=kafka_broker_address)

    # Define a topic where trades are pushed to
    topic = app.topic(name=kafka_topic, value_serializer="json")

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            if len(trades) > 0:
                for trade in trades:
                    # serialize trades as bytes
                    message = topic.serialize(key=trade.pair, value=trade.to_dict())

                    # push to topic
                    producer.produce(
                        topic=topic.name, key=message.key, value=message.value
                    )

                    logger.info(f"Pushed trade to Kafka: {trade}")


if __name__ == "__main__":
    from config import config

    # initialise Kraken API
    kraken_client = KrakenWebsocketApi(pairs=config.pairs)

    main(config.kafka_broker_address, config.kafka_topic, kraken_client)
