from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    num_candles_in_state: int,
):
    """
    Service for ingesting candle data, computes indicator data, and pushing to a topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_input_topic (str): The name of the input topic.
        kafka_output_topic (str): The name of the output topic.
        kafka_consumer_group (str): The name of the consumer group.
        num_candles_in_state (int): The number of candles to use for technical indicator calculations.

    """

    logger.info("Starting technical indicators service")

    # initialise quixstreams application
    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    # define topics
    candles_topic = app.topic(name=kafka_input_topic, value_deserializer="json")
    indicators_topic = app.topic(name=kafka_output_topic, value_deserializer="json")

    # create a streaming dataframe from the input topic that pushes to output topic
    sdf = app.dataframe(topic=candles_topic)
    sdf.to_topic(indicators_topic)

    # run the application
    app.run()


if __name__ == "__main__":
    from config import config

    main(main(**config.__dict__))
