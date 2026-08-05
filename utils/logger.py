"""
Logging Framework for NeuroLearn Research Suite.
Provides structured research logging with console and file output.
"""

import logging
import os
import sys
from typing import Optional


def get_logger(name: str = "NeuroLearn", log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """Retrieve or configure a logger instance for research tracking."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Console Handler
        c_handler = logging.StreamHandler(sys.stdout)
        c_format = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

        # Optional File Handler
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            f_handler = logging.FileHandler(log_file, encoding="utf-8")
            f_format = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s")
            f_handler.setFormatter(f_format)
            logger.addHandler(f_handler)

    return logger
