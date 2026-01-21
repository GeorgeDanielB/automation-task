"""Page Object for the Checkout pages."""

from dataclasses import dataclass
from typing import Optional

import allure

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class OrderSummary:
    """Order summary information."""
    item_total: float
    tax: float
    total: float


class CheckoutPage(BasePage):
    URL_PATH = "/checkout-step-one.html"
    PAGE_TITLE = "Swag Labs"

    # Locators - Step One
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CANCEL_BUTTON = "#cancel"
    CONTINUE_BUTTON = "#continue"

    # Locators - Step Two
    FINISH_BUTTON = "#finish"
    SUMMARY_INFO = ".summary_info"
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"

    # Locators - Complete
    BACK_HOME_BUTTON = "#back-to-products"
    COMPLETE_HEADER = ".complete-header"
    CHECKOUT_COMPLETE_CONTAINER = "#checkout_complete_container"

    # Error
    ERROR_MESSAGE = "[data-test='error']"

    # Step One: Information

    @allure.step("Fill checkout information")
    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill in the checkout information form."""
        logger.info("Filling checkout information")
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)

    @allure.step("Continue to step two")
    def continue_to_overview(self) -> None:
        """Continue from step one to step two."""
        self.click(self.CONTINUE_BUTTON)

    # Step Two: Overview

    @allure.step("Finish checkout")
    def finish_checkout(self) -> None:
        """Complete the checkout process."""
        logger.info("Finishing checkout")
        self.click(self.FINISH_BUTTON)

    def get_order_summary(self) -> Optional[OrderSummary]:
        """Get the order summary information."""
        if not self.is_visible(self.SUMMARY_INFO):
            return None

        item_total = float(self.get_text(self.ITEM_TOTAL).split("$")[1])
        tax = float(self.get_text(self.TAX).split("$")[1])
        total = float(self.get_text(self.TOTAL).split("$")[1])

        return OrderSummary(item_total=item_total, tax=tax, total=total)

    # Completion

    def get_confirmation_header(self) -> str:
        """Get the order confirmation header text."""
        if self.is_visible(self.COMPLETE_HEADER):
            return self.get_text(self.COMPLETE_HEADER)
        return ""

    @allure.step("Return to products")
    def back_to_products(self) -> None:
        """Return to products page after completing checkout."""
        self.click(self.BACK_HOME_BUTTON)

    # Navigation

    @allure.step("Cancel checkout")
    def cancel(self) -> None:
        """Cancel the checkout process."""
        self.click(self.CANCEL_BUTTON)

    # Error Handling

    def get_error_message(self) -> str:
        """Get the current error message."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_error_displayed(self) -> bool:
        """Check if an error is displayed."""
        return self.is_visible(self.ERROR_MESSAGE)

    # Validations

    @allure.step("Verify step one is loaded")
    def is_step_one_loaded(self) -> bool:
        """Verify checkout step one is loaded."""
        return (
            self.is_visible(self.FIRST_NAME_INPUT) and
            self.is_visible(self.CONTINUE_BUTTON)
        )

    @allure.step("Verify step two is loaded")
    def is_step_two_loaded(self) -> bool:
        """Verify checkout step two is loaded."""
        return (
            self.is_visible(self.SUMMARY_INFO) and
            self.is_visible(self.FINISH_BUTTON)
        )

    @allure.step("Verify checkout is complete")
    def is_checkout_complete(self) -> bool:
        """Verify checkout has been completed."""
        return self.is_visible(self.CHECKOUT_COMPLETE_CONTAINER)