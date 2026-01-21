"""
Element Handler Module.

Provides a wrapper around Playwright's element interactions with
enhanced error handling, logging, and retry capabilities.
"""

from typing import List, Optional, Union

from playwright.sync_api import ElementHandle, Locator, Page, TimeoutError as PlaywrightTimeout

from utils.logger import get_logger

logger = get_logger(__name__)


class ElementHandler:
    """Wrapper for Playwright element interactions."""

    def __init__(self, page: Page, screenshot_on_error: bool = True):
        self._page = page
        self._screenshot_on_error = screenshot_on_error

    @property
    def page(self) -> Page:
        """Get the underlying page instance."""
        return self._page

    def _get_locator(self, selector: str) -> Locator:
        """Get a locator for the given selector."""
        return self._page.locator(selector)

    def _handle_error(self, action: str, selector: str, error: Exception) -> None:
        """Handle interaction errors with logging."""
        logger.error(f"Failed to {action} on '{selector}': {error}")

    def click(
        self,
        selector: str,
        *,
        timeout: Optional[float] = None,
        force: bool = False,
        click_count: int = 1,
    ) -> None:
        """Click on an element."""
        logger.debug(f"Clicking on '{selector}'")
        try:
            locator = self._get_locator(selector)
            locator.click(timeout=timeout, force=force, click_count=click_count)
            logger.debug(f"Successfully clicked on '{selector}'")
        except PlaywrightTimeout as e:
            self._handle_error("click", selector, e)
            raise

    def fill(
        self,
        selector: str,
        value: str,
        *,
        timeout: Optional[float] = None,
        clear_first: bool = True,
    ) -> None:
        """Fill an input field with text."""
        logger.debug(f"Filling '{selector}' with '{value[:20]}...' " if len(value) > 20 else f"Filling '{selector}' with '{value}'")
        try:
            locator = self._get_locator(selector)
            if clear_first:
                locator.clear(timeout=timeout)
            locator.fill(value, timeout=timeout)
            logger.debug(f"Successfully filled '{selector}'")
        except PlaywrightTimeout as e:
            self._handle_error("fill", selector, e)
            raise

    def get_text(self, selector: str, *, timeout: Optional[float] = None) -> str:
        """Get text content of an element."""
        logger.debug(f"Getting text from '{selector}'")
        try:
            locator = self._get_locator(selector)
            text = locator.text_content(timeout=timeout) or ""
            logger.debug(f"Got text: '{text[:50]}...'" if len(text) > 50 else f"Got text: '{text}'")
            return text
        except PlaywrightTimeout as e:
            self._handle_error("get_text", selector, e)
            raise

    def get_attribute(
        self,
        selector: str,
        attribute: str,
        *,
        timeout: Optional[float] = None,
    ) -> Optional[str]:
        """Get an attribute value from an element."""
        logger.debug(f"Getting attribute '{attribute}' from '{selector}'")
        try:
            locator = self._get_locator(selector)
            return locator.get_attribute(attribute, timeout=timeout)
        except PlaywrightTimeout as e:
            self._handle_error("get_attribute", selector, e)
            raise

    def get_input_value(self, selector: str, *, timeout: Optional[float] = None) -> str:
        """Get the value of an input field."""
        logger.debug(f"Getting input value from '{selector}'")
        try:
            locator = self._get_locator(selector)
            return locator.input_value(timeout=timeout)
        except PlaywrightTimeout as e:
            self._handle_error("get_input_value", selector, e)
            raise

    def is_visible(self, selector: str, *, timeout: Optional[float] = None) -> bool:
        """Check if an element is visible."""
        try:
            locator = self._get_locator(selector)
            return locator.is_visible(timeout=timeout)
        except PlaywrightTimeout:
            return False

    def is_enabled(self, selector: str, *, timeout: Optional[float] = None) -> bool:
        """Check if an element is enabled."""
        try:
            locator = self._get_locator(selector)
            return locator.is_enabled(timeout=timeout)
        except PlaywrightTimeout:
            return False

    def wait_for_visible(
        self,
        selector: str,
        *,
        timeout: Optional[float] = None,
    ) -> Locator:
        """Wait for an element to be visible."""
        logger.debug(f"Waiting for '{selector}' to be visible")
        locator = self._get_locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def wait_for_hidden(
        self,
        selector: str,
        *,
        timeout: Optional[float] = None,
    ) -> None:
        """Wait for an element to be hidden."""
        logger.debug(f"Waiting for '{selector}' to be hidden")
        locator = self._get_locator(selector)
        locator.wait_for(state="hidden", timeout=timeout)

    def select_option(
        self,
        selector: str,
        value: Optional[str] = None,
        *,
        label: Optional[str] = None,
        index: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> List[str]:
        """Select option(s) from a dropdown."""
        logger.debug(f"Selecting option in '{selector}'")
        locator = self._get_locator(selector)
        
        if value is not None:
            return locator.select_option(value=value, timeout=timeout)
        elif label is not None:
            return locator.select_option(label=label, timeout=timeout)
        elif index is not None:
            return locator.select_option(index=index, timeout=timeout)
        else:
            raise ValueError("Must provide value, label, or index")

    def get_all_texts(self, selector: str) -> List[str]:
        """Get text content from all matching elements."""
        locator = self._get_locator(selector)
        return locator.all_text_contents()

    def count(self, selector: str) -> int:
        """Count matching elements."""
        locator = self._get_locator(selector)
        return locator.count()