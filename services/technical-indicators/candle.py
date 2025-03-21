from config import config
from loguru import logger
from quixstreams import State

MAX_CANDLES_IN_STATE = config.max_candles_in_state


def is_same_window(new_candle: dict, last_candle: dict) -> bool:
    """
    Checks if the new candle received is in the same window as the last recorded candle.

    Args:
        new_candle (dict): The latest candle.
        last_candle (dict): The last candle in the candles list.

    Returns:
        bool
    """

    return (
        new_candle["window_start_ms"] == last_candle["window_start_ms"]
        and new_candle["window_end_ms"] == last_candle["window_end_ms"]
    )


def update_candles(candle: dict, state: State) -> None:
    """
    Fetch candles list from state and updates it with the latest candle.

    If the candle corresponds to a new window, append it to the list.
    Else, replace the last candle with updated data.

    Args:
        candle (dict): The latest candle.
        state (State): The application state.

    Returns:
        None
    """

    candles = state.get("candles", default=[])

    if not candles or not is_same_window(candle, candles[-1]):
        candles.append(candle)
    else:
        candles[-1] = candle

    logger.debug(f"No of candles in state: {len(candles)}")

    # remove candles from the start of list as the window limit is reached
    if len(candles) > MAX_CANDLES_IN_STATE:
        candles.pop(0)

    state.set("candles", candles)
