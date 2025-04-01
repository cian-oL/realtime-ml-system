import numpy as np
from quixstreams import State
from talib import stream


def compute_indicators(candle: dict, state: State) -> dict:
    """
    Compute the technical data from candles in the state.

    Indicators included:
        The Simple Moving Average (SMA)
        The Relative Strength Index (RSI)
        The Exponential Moving Average (EMA)
        Bollinger Bands

    Args:
        candle (dict): _description_
        state (State): _description_

    Returns:
        A dictionary of the technical indicators with the latest candle data tagged
    """

    candles = state.get("candles", [])

    # extract candle parameters from current state
    close = np.asarray([candle["close"] for candle in candles])

    # indicators
    indicators = {}
    indicators["sma_14"] = stream.SMA(close, timeperiod=14)
    indicators["rsi_14"] = stream.RSI(close, timeperiod=14)
    indicators["ema_10"] = stream.EMA(close, timeperiod=10)
    indicators["b_bands_14"] = stream.BBANDS(
        close, timeperiod=14, nbdevup=2, nbdevdn=2, matype=0
    )

    breakpoint()

    return {**candle, **indicators}
