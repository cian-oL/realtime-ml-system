from datetime import timedelta
from typing import Any, List, Optional, Tuple

from loguru import logger
from quixstreams import Application
from quixstreams.models import TimestampType


def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload
    instead of Kafka timestamp.

    Returns:
        int: The timestamp extracted from the message payload.
    """

    return value["timestamp_ms"]


def init_candle(trade: dict) -> dict:
    """
    Initializes a new candle from the first trade.

    Args:
        trade (dict): The trade to initialize the candle from.

    Returns:
        dict: The initialized candle.
    """

    return {
        "open": trade["price"],
        "high": trade["price"],
        "low": trade["price"],
        "close": trade["price"],
        "volume": trade["volume"],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Updates a candle with new trade data.

    Args:
        candle (dict): The candle to update.
        trade (dict): The new trade data.

    Returns:
        dict: The updated candle.
    """

    candle["high"] = max(candle["high"], trade["price"])
    candle["low"] = min(candle["low"], trade["price"])
    candle["close"] = trade["price"]
    candle["volume"] += trade["volume"]

    return candle


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
):
    """
    Service for ingesting trades from a topic, generating candlees, and pushing them to a topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_input_topic (str): The name of the input topic.
        kafka_output_topic (str): The name of the output topic.
        kafka_consumer_group (str): The name of the consumer group.
        candle_seconds (int): The timeframe of the candle data in seconds.

    """
    logger.info("Starting candles service")

    # initialise quixstreams application
    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    # define topics
    trades_topic = app.topic(
        name=kafka_input_topic,
        timestamp_extractor=custom_ts_extractor,
        value_deserializer="json",
    )
    candles_topic = app.topic(name=kafka_output_topic, value_serializer="json")

    # create a streaming dataframe from the input topic that pushes to output topic
    # emit all intermediate candles to make system more responsive
    sdf = app.dataframe(topic=trades_topic)

    sdf = (
        sdf.tumbling_window(timedelta(seconds=candle_seconds))
        .reduce(reducer=update_candle, initializer=init_candle)
        .current()
        .to_topic(topic=candles_topic)
    )

    # run the application
    app.run()


if __name__ == "__main__":
    from config import config

    main(**config.__dict__)
