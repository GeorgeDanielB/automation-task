"""
Checkout Regression Test Suite.

Comprehensive tests for the checkout flow on SauceDemo.
"""

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.epic("Checkout")
@allure.feature("Checkout Information")
class TestCheckoutInformationRegression:
    """Regression tests for checkout information step."""

    @allure.story("Page Load")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_checkout_step_one_loads(self, checkout_page: CheckoutPage):
        """Verify checkout step one loads correctly."""
        assert checkout_page.is_step_one_loaded()

    @allure.story("Valid Information")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_can_proceed_with_valid_information(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify can proceed to step two with valid info."""
        checkout_page.fill_information(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_to_overview()

        assert checkout_page.is_step_two_loaded()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_error_when_first_name_missing(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify error when first name is empty."""
        checkout_page.fill_information("", checkout_data["last_name"], checkout_data["postal_code"])
        checkout_page.continue_to_overview()

        assert checkout_page.is_error_displayed()
        assert "first name" in checkout_page.get_error_message().lower()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_error_when_last_name_missing(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify error when last name is empty."""
        checkout_page.fill_information(checkout_data["first_name"], "", checkout_data["postal_code"])
        checkout_page.continue_to_overview()

        assert checkout_page.is_error_displayed()
        assert "last name" in checkout_page.get_error_message().lower()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_error_when_postal_code_missing(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify error when postal code is empty."""
        checkout_page.fill_information(checkout_data["first_name"], checkout_data["last_name"], "")
        checkout_page.continue_to_overview()

        assert checkout_page.is_error_displayed()
        assert "postal code" in checkout_page.get_error_message().lower()

    @allure.story("Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cancel_returns_to_cart(self, checkout_page: CheckoutPage):
        """Verify cancel returns to cart page."""
        checkout_page.cancel()

        cart_page = CartPage(checkout_page.page)
        assert cart_page.is_loaded()


@allure.epic("Checkout")
@allure.feature("Checkout Overview")
class TestCheckoutOverviewRegression:
    """Regression tests for checkout overview step."""

    @allure.story("Order Summary")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_order_summary_shows_totals(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify order summary displays totals."""
        checkout_page.fill_information(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_to_overview()

        summary = checkout_page.get_order_summary()

        assert summary is not None
        assert summary.item_total > 0
        assert summary.tax > 0
        assert summary.total > 0

    @allure.story("Order Summary")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_order_total_equals_items_plus_tax(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify total equals items + tax."""
        checkout_page.fill_information(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_to_overview()

        summary = checkout_page.get_order_summary()
        expected_total = summary.item_total + summary.tax

        assert abs(summary.total - expected_total) < 0.01


@allure.epic("Checkout")
@allure.feature("Checkout Completion")
class TestCheckoutCompletionRegression:
    """Regression tests for checkout completion."""

    @allure.story("Complete Order")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_complete_checkout_successfully(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify checkout can be completed successfully."""
        checkout_page.fill_information(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_to_overview()
        checkout_page.finish_checkout()

        assert checkout_page.is_checkout_complete()

    @allure.story("Confirmation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_confirmation_shows_thank_you_message(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify confirmation page shows thank you message."""
        checkout_page.fill_information(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_to_overview()
        checkout_page.finish_checkout()

        assert "thank you" in checkout_page.get_confirmation_header().lower()

    @allure.story("Post-Checkout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_back_home_returns_to_inventory(self, checkout_page: CheckoutPage, checkout_data: dict):
        """Verify Back Home button returns to inventory."""
        checkout_page.fill_information(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_to_overview()
        checkout_page.finish_checkout()
        checkout_page.back_to_products()

        inventory_page = InventoryPage(checkout_page.page)
        assert inventory_page.is_loaded()


@allure.epic("Checkout")
@allure.feature("End-to-End Flow")
class TestCheckoutE2ERegression:
    """End-to-end checkout flow tests."""

    @allure.story("Full Purchase Flow")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_complete_purchase_flow(self, inventory_page: InventoryPage, products: dict, checkout_data: dict):
        """Verify complete purchase flow from start to finish."""
        # Add item
        inventory_page.add_product_to_cart(products["backpack"]["name"])

        # Go to cart
        inventory_page.go_to_cart()
        cart_page = CartPage(inventory_page.page)
        assert cart_page.get_item_count() == 1

        # Checkout
        cart_page.proceed_to_checkout()
        checkout_page = CheckoutPage(inventory_page.page)
        checkout_page.fill_information(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.continue_to_overview()
        checkout_page.finish_checkout()

        assert checkout_page.is_checkout_complete()