"""
Logging Configuration Module.

Provides centralized logging setup for the framework.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class TestContextFilter(logging.Filter):
    """Filter that adds test context to log records."""

    _current_test: Optional[str] = None

    @classmethod
    def set_current_test(cls, test_name: Optional[str]) -> None:
        """Set the current test name."""
        cls._current_test = test_name

    def filter(self, record: logging.LogRecord) -> bool:
        """Add test context to record."""
        record.test_name = self._current_test or "framework"
        return True


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Set up logging for the framework."""
    logger = logging.getLogger("qa_framework")
    logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    if logger.hasHandlers():
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()

    # Add test context filter
    context_filter = TestContextFilter()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.addFilter(context_filter)

    console_format = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    console_handler.setFormatter(logging.Formatter(console_format, "%H:%M:%S"))

    logger.addHandler(console_handler)

    # File handler
    log_dir = Path("reports")
    log_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"test_run_{date_str}.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.addFilter(context_filter)

    file_format = "%(asctime)s [%(levelname)-8s] [%(test_name)s] %(name)s: %(message)s"
    file_handler.setFormatter(logging.Formatter(file_format, "%Y-%m-%d %H:%M:%S"))

    logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module."""
    root_logger = logging.getLogger("qa_framework")
    if not root_logger.handlers:
        setup_logging()

    return logging.getLogger(f"qa_framework.{name}")