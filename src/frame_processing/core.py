from loguru import logger

from src.data_transmission.core import get_current_frame_data


def run_frame_processing() -> None:
    logger.info("Start frame processing")
    while True:
        current_frame_data = get_current_frame_data()
        # TODO: Implement frame processing logic
        logger.debug(f"Current frame data: {current_frame_data}")
        break  # For testing purposes
