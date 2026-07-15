"""
File Handler Module.

Provides utilities for reading test data files.
"""

from pathlib import Path
from typing import Any

import yaml

from utils.logger import get_logger

logger = get_logger(__name__)


class FileHandler:
    """Utility class for file operations."""

    @staticmethod
    def read_yaml(file_path: str | Path) -> dict[str, Any]:
        """Read a YAML file."""
        path = Path(file_path)
        logger.debug(f"Reading YAML file: {path}")

        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {path}")

        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
