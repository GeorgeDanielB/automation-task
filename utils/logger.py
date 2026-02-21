"""Logging Configuration Module."""

import logging
import sys
import threading

from datetime import datetime
from pathlib import Path
from typing import Optional

_setup_lock = threading.Lock()
_is_setup = False

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
    global _is_setup

    with _setup_lock:
        if _is_setup:
            return logging.getLogger("qa_framework")

        logger = logging.getLogger("qa_framework")
        logger.setLevel(getattr(logging, level.upper()))

        context_filter = TestContextFilter()

        # Console handler

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.DEBUG)
        console.addFilter(context_filter)
        console.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s", "%H:%M:%S",
        ))
        logger.addHandler(console)

        # File handler

        log_dir = Path("reports")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"test_run_{datetime.now():%Y-%m-%d}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.addFilter(context_filter)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)-8s] [%(test_name)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        ))
        logger.addHandler(file_handler)

        _is_setup = True
        return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module."""
    root = logging.getLogger("qa_framework")
    if not root.handlers:
        setup_logging()

    return logging.getLogger(f"qa_framework.{name}")