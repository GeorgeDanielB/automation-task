"""
Shopping Cart Regression Test Suite.

Comprehensive tests for the cart page functionality on SauceDemo.
"""

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.epic("Shopping Cart")
@allure.feature("Cart Page")
class TestCartPageRegression:
    """Regression tests for cart page functionality."""

    @allure.story("Cart Display")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_cart_page_loads_correctly(self, inventory_page: InventoryPage):
        """Verify cart page loads with all elements."""
        inventory_page.go_to_cart()
        cart_page = CartPage(inventory_page.page)
        
        assert cart_page.is_loaded()

    @allure.story("Cart Display")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_cart_shows_added_products(self, inventory_page: InventoryPage, products: dict):
        """Verify cart displays products that were added."""
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.add_product_to_cart(products["bike_light"]["name"])
        inventory_page.go_to_cart()
        
        cart_page = CartPage(inventory_page.page)
        
        assert cart_page.get_item_count() == 2
        assert cart_page.contains_item(products["backpack"]["name"])
        assert cart_page.contains_item(products["bike_light"]["name"])

    @allure.story("Cart Display")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_shows_correct_product_details(self, inventory_page: InventoryPage, products: dict):
        """Verify cart shows correct product name and price."""
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.go_to_cart()
        
        cart_page = CartPage(inventory_page.page)
        item = cart_page.get_cart_item(products["backpack"]["name"])
        
        assert item is not None
        assert item.name == products["backpack"]["name"]
        assert item.price == products["backpack"]["price"]

    @allure.story("Empty Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_empty_cart_displays_correctly(self, inventory_page: InventoryPage):
        """Verify empty cart page displays correctly."""
        inventory_page.go_to_cart()
        cart_page = CartPage(inventory_page.page)
        
        assert cart_page.is_empty()


@allure.epic("Shopping Cart")
@allure.feature("Cart Operations")
class TestCartOperationsRegression:
    """Regression tests for cart operations."""

    @allure.story("Remove Item")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_remove_item_from_cart_page(self, inventory_page: InventoryPage, products: dict):
        """Verify can remove item from cart page."""
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.go_to_cart()
        
        cart_page = CartPage(inventory_page.page)
        cart_page.remove_item(products["backpack"]["name"])
        
        assert cart_page.is_empty()

    @allure.story("Remove Item")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_remove_one_item_keeps_others(self, inventory_page: InventoryPage, products: dict):
        """Verify removing one item doesn't affect other items."""
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.add_product_to_cart(products["bike_light"]["name"])
        inventory_page.go_to_cart()
        
        cart_page = CartPage(inventory_page.page)
        cart_page.remove_item(products["backpack"]["name"])
        
        assert cart_page.get_item_count() == 1
        assert cart_page.contains_item(products["bike_light"]["name"])


@allure.epic("Shopping Cart")
@allure.feature("Cart Navigation")
class TestCartNavigationRegression:
    """Regression tests for cart navigation."""

    @allure.story("Continue Shopping")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_continue_shopping_returns_to_inventory(self, inventory_page: InventoryPage):
        """Verify Continue Shopping returns to inventory."""
        inventory_page.go_to_cart()
        cart_page = CartPage(inventory_page.page)
        
        cart_page.continue_shopping()
        
        assert inventory_page.is_loaded()

    @allure.story("Proceed to Checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_checkout_button_proceeds_to_checkout(self, inventory_page: InventoryPage, products: dict):
        """Verify Checkout button proceeds to checkout page."""
        inventory_page.add_product_to_cart(products["backpack"]["name"])
        inventory_page.go_to_cart()
        
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded()
