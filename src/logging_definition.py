import logging
import sys


def log_setup(file_name: str = "general.log") -> None:
    """
    Standard defintion for all logging in the PiPetal project.
    Allows all independent start scripts to use the same config setup

    Args:
        file_name (string): The name of the log file.

    Returns: None
    """
    logging.basicConfig(
        handlers=[
            logging.FileHandler(file_name, mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)-8s - %(message)-50s [%(name)s.%(funcName)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
