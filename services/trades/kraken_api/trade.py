from datetime import datetime

from pydantic import BaseModel


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

    def to_dict(self) -> dict:
        """
        transforms object into a dictionary

        Returns:
            dict: Dictionary of trade info for pipeline transfer
        """
        data = self.model_dump()
        data["timestamp"] = (
            self.timestamp.isoformat()
        )  # because datetime.datetime is not JSON serializable

        return data
