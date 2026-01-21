"""Base Page Module."""

from typing import List

from playwright.sync_api import Page

from config.settings import get_settings
from core.element_handler import ElementHandler
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Base class for all Page Objects."""

    URL_PATH: str = ""

    def __init__(self, page: Page):
        self._page = page
        self._settings = get_settings()
        self._element_handler = ElementHandler(page)

    @property
    def page(self) -> Page:
        """Get the underlying Playwright page."""
        return self._page

    @property
    def url(self) -> str:
        """Get the full URL for this page."""
        return f"{self._settings.base_url}{self.URL_PATH}"

    @property
    def current_url(self) -> str:
        """Get the current page URL."""
        return self._page.url

    # Navigation

    def navigate(self) -> None:
        """Navigate to this page's URL."""
        logger.info(f"Navigating to {self.__class__.__name__}: {self.url}")
        self._page.goto(self.url)

    # Element Interactions

    def click(self, selector: str, **kwargs) -> None:
        """Click on an element."""
        self._element_handler.click(selector, **kwargs)

    def fill(self, selector: str, value: str, **kwargs) -> None:
        """Fill an input field."""
        self._element_handler.fill(selector, value, **kwargs)

    def get_text(self, selector: str, **kwargs) -> str:
        """Get text content of an element."""
        return self._element_handler.get_text(selector, **kwargs)

    def is_visible(self, selector: str, **kwargs) -> bool:
        """Check if element is visible."""
        return self._element_handler.is_visible(selector, **kwargs)

    def wait_for_visible(self, selector: str, **kwargs):
        """Wait for element to be visible."""
        return self._element_handler.wait_for_visible(selector, **kwargs)

    def wait_for_hidden(self, selector: str, **kwargs) -> None:
        """Wait for element to be hidden."""
        self._element_handler.wait_for_hidden(selector, **kwargs)

    def select_option(self, selector: str, **kwargs) -> List[str]:
        """Select option from dropdown."""
        return self._element_handler.select_option(selector, **kwargs)

    def get_all_texts(self, selector: str) -> List[str]:
        """Get text from all matching elements."""
        return self._element_handler.get_all_texts(selector)

    def count(self, selector: str) -> int:
        """Count matching elements."""
        return self._element_handler.count(selector)

    # Waits

    def wait_for_load_state(self, state: str = "networkidle") -> None:
        """Wait for page to reach a specific load state."""
        self._page.wait_for_load_state(state)