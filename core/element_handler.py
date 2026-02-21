"""
Element Handler Module.

Provides a wrapper around Playwright's element interactions with
enhanced error handling, logging, and screenshot capture on failure.
"""

import functools
import time
from pathlib import Path
from typing import Callable, List, Optional

from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeout

from utils.logger import get_logger

logger = get_logger(__name__)

SCREENSHOTS_DIR = Path("screenshots")

def _with_error_handling(action_name: str):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self: "ElementHandler", selector: str, *args, **kwargs):
            try:
                return func(self, selector, *args, **kwargs)
            except PlaywrightTimeout as e:
                logger.error(f"Failed to {action_name} on '{selector}': {e}")
                self._capture_error_screenshot(action_name, selector)
                raise
        return wrapper
    return decorator

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

    def _capture_error_screenshot(self, action: str, selector: str) -> None:
        if not self._screenshot_on_error:
            return
        try:
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = int(time.time())
            safe_selector = selector[:40].replace("/", "_").replace(" ", "_")
            path = SCREENSHOTS_DIR / f"error_{action}_{safe_selector}_{timestamp}.png"
            self._page.screenshot(path=str(path))
            logger.debug(f"Error screenshot saved: {path}")
        except Exception as e:
            logger.warning(f"Could not capture error screenshot: {e}")

    # Element Interactions

    @_with_error_handling("click")
    def click(
        self,
        selector: str,
        *,
        timeout: Optional[float] = None,
        force: bool = False,
        click_count: int = 1,
    ) -> None:
        """Click on an element."""
        logger.debug(f"Clicking '{selector}'")
        self._get_locator(selector).click(
            timeout=timeout, force=force, click_count=click_count,
        )

    @_with_error_handling("fill")
    def fill(
        self,
        selector: str,
        value: str,
        *,
        timeout: Optional[float] = None,
        clear_first: bool = True,
    ) -> None:
        """Fill an input field with text."""
        display = value[:20] + "..." if len(value) > 20 else value
        logger.debug(f"Filling '{selector}' with '{display}'")
        locator = self._get_locator(selector)
        if clear_first:
            locator.clear(timeout=timeout)
        locator.fill(value, timeout=timeout)

    @_with_error_handling("get_text")
    def get_text(self, selector: str, *, timeout: Optional[float] = None) -> str:
        """Get text content of an element."""
        text = self._get_locator(selector).text_content(timeout=timeout) or ""
        display = text[:50] + "..." if len(text) > 50 else text
        logger.debug(f"Text from '{selector}': '{display}'")
        return text

    @_with_error_handling("get_attribute")
    def get_attribute(
        self,
        selector: str,
        attribute: str,
        *,
        timeout: Optional[float] = None,
    ) -> Optional[str]:
        """Get an attribute value from an element."""
        logger.debug(f"Getting '{attribute}' from '{selector}'")
        return self._get_locator(selector).get_attribute(attribute, timeout=timeout)

    @_with_error_handling("get_input_value")
    def get_input_value(self, selector: str, *, timeout: Optional[float] = None) -> str:
        """Get the value of an input field."""
        return self._get_locator(selector).input_value(timeout=timeout)

    def is_visible(self, selector: str, *, timeout: Optional[float] = None) -> bool:
        """Check if an element is visible."""
        return self._get_locator(selector).is_visible(timeout=timeout)

    def is_enabled(self, selector: str, *, timeout: Optional[float] = None) -> bool:
        """Check if an element is enabled."""
        return self._get_locator(selector).is_enabled(timeout=timeout)

    # Waits

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
        self._get_locator(selector).wait_for(state="hidden", timeout=timeout)

    # Dropdowns

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
        if label is not None:
            return locator.select_option(label=label, timeout=timeout)
        if index is not None:
            return locator.select_option(index=index, timeout=timeout)
        raise ValueError("Must provide value, label, or index")

    def get_all_texts(self, selector: str) -> List[str]:
        """Get text content from all matching elements."""
        return self._get_locator(selector).all_text_contents()

    def count(self, selector: str) -> int:
        """Count matching elements."""
        return self._get_locator(selector).count()