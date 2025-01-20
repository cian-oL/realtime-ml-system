import json
from typing import List
from loguru import logger
from websocket import create_connection

from .trade import Trade


class KrakenWebsocketApi:
    """
    API source: https://docs.kraken.com/api/docs/websocket-v2/trade
    """

    KRAKEN_WEBSOCKET_URL = "wss://ws.kraken.com/v2"

    def __init__(self, pairs: List[str]) -> None:
        self.pairs = pairs

        # subscribe to websocket
        self._subscribe(self.KRAKEN_WEBSOCKET_URL)

    def _subscribe(self, websocket_url: str) -> None:
        """
        Subscribes to the websocket by connection via url and awaits initial snapshot
        """
        self.ws_client = create_connection(websocket_url)
        self.ws_client.send(
            json.dumps(
                {
                    "method": "subscribe",
                    "params": {
                        "channel": "trade",
                        "symbol": self.pairs,
                        "snapshot": True,
                    },
                }
            )
        )
        # discard first two confirmation methods from API
        for i in range(0, len(self.pairs)):
            _ = self.ws_client.recv()
            _ = self.ws_client.recv()
            i += 1

        print(self.ws_client.recv())

    def get_trades(self) -> List[Trade]:
        """
        Returns a list of fetched trades from the websocket API

        Returns:
            List[Trade]: A list of trade objects
        """

        # deserialise data from the websocket and extract trades data
        try:
            data = json.loads(self.ws_client.recv())
        except json.JSONDecodeError as err:
            logger.error(f"Error decoding JSON: {err}")
            return []

        # handle received payloads without trades_data (channel == "heartbeat")
        if data["channel"] == "heartbeat":
            return []

        if data["channel"] == "trade":
            trades_data = data["data"]

            trades = [
                Trade(
                    pair=trade["symbol"],
                    price=trade["price"],
                    volume=trade["qty"],
                    timestamp=trade["timestamp"],
                )
                for trade in trades_data
            ]

            return trades
