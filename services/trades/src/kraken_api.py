"""
Module for interacting with the Kraken cryptocurrency exchange API.
It provides a mock implementation of the Kraken API trade data
structures using Pydantic models for data validation.
"""

from datetime import datetime
from pydantic import BaseModel
from typing import List


class Trade(BaseModel):
    """

    Args:
        BaseModel (_type_): _description_
    """

    pair: str
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: int


class KrakenMockAPI:
    """
    API source: https://docs.kraken.com/api/docs/websocket-v2/trade
    """

    def __init__(self, pair: str) -> None:
        self.pair = pair

    def get_trades(self) -> List[Trade]:
        """
        Returns a list of mock trades.
        """

        mock_trades = [
            Trade(
                pair=self.pair,
                price=35485.2,
                volume=0.01,
                timestamp=datetime(2023, 2, 10, 15, 30, 0),
                timestamp_ms=1676055000000,
            ),
            Trade(
                pair=self.pair,
                price=35490.1,
                volume=0.005,
                timestamp=datetime(2023, 2, 10, 15, 31, 0),
                timestamp_ms=1676055060000,
            ),
        ]

        return mock_trades
