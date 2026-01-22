"""
Inventory/Products Regression Test Suite.

Comprehensive tests for the product catalog functionality on SauceDemo.
"""

import allure
import pytest

from pages.inventory_page import InventoryPage, SortOrder
from pages.cart_page import CartPage


@allure.epic("Product Catalog")
@allure.feature("Product Display")
class TestProductDisplayRegression:
    """Regression tests for product display functionality."""

    @allure.story("Product Listing")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_inventory_displays_all_products(self, inventory_page: InventoryPage):
        """Verify all 6 products are displayed."""
        assert inventory_page.is_loaded()
        assert inventory_page.get_product_count() == 6

    @allure.story("Product Information")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_products_have_name_description_price(self, inventory_page: InventoryPage):
        """Verify each product displays name, description, and price."""
        products = inventory_page.get_all_products()

        for product in products:
            assert product.name
            assert product.description
            assert product.price > 0

    @allure.story("Product Information")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_product_prices_are_correct(self, inventory_page: InventoryPage, products: dict):
        """Verify known product prices are accurate."""
        backpack = inventory_page.get_product_info(products["backpack"]["name"])
        bike_light = inventory_page.get_product_info(products["bike_light"]["name"])

        assert backpack.price == products["backpack"]["price"]
        assert bike_light.price == products["bike_light"]["price"]

    @allure.story("Product Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_can_click_product_to_view_details(self, inventory_page: InventoryPage, products: dict):
        """Verify clicking product navigates to detail page."""
        inventory_page.click_product(products["backpack"]["name"])

        assert "inventory-item" in inventory_page.current_url


@allure.epic("Product Catalog")
@allure.feature("Product Sorting")
class TestProductSortingRegression:
    """Regression tests for product sorting functionality."""

    @allure.story("Sort by Name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_name_a_to_z(self, inventory_page: InventoryPage):
        """Verify products can be sorted A-Z."""
        inventory_page.sort_products(SortOrder.NAME_ASC)

        names = inventory_page.get_product_names()
        assert names == sorted(names)

    @allure.story("Sort by Name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_name_z_to_a(self, inventory_page: InventoryPage):
        """Verify products can be sorted Z-A."""
        inventory_page.sort_products(SortOrder.NAME_DESC)

        names = inventory_page.get_product_names()
        assert names == sorted(names, reverse=True)

    @allure.story("Sort by Price")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_price_low_to_high(self, inventory_page: InventoryPage):
        """Verify products can be sorted by price ascending."""
        inventory_page.sort_products(SortOrder.PRICE_LOW_HIGH)

        prices = inventory_page.get_product_prices()
        assert prices == sorted(prices)

    @allure.story("Sort by Price")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_price_high_to_low(self, inventory_page: InventoryPage):
        """Verify products can be sorted by price descending."""
        inventory_page.sort_products(SortOrder.PRICE_HIGH_LOW)

        prices = inventory_page.get_product_prices()
        assert prices == sorted(prices, reverse=True)


@allure.epic("Shopping Cart")
@allure.feature("Add to Cart")
class TestAddToCartRegression:
    """Regression tests for add to cart functionality."""

    @allure.story("Add Single Product")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_single_product_to_cart(self, inventory_page: InventoryPage, products: dict):
        """Verify can add a single product to cart."""
        product_name = products["backpack"]["name"]
        inventory_page.add_product_to_cart(product_name)

        assert inventory_page.get_cart_count() == 1
        assert inventory_page.is_product_in_cart(product_name)

    @allure.story("Add Multiple Products")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_add_multiple_products_to_cart(self, inventory_page: InventoryPage, products: dict):
        """Verify can add multiple products to cart."""
        product_names = [
            products["backpack"]["name"],
            products["bike_light"]["name"],
            products["bolt_tshirt"]["name"]
        ]

        for name in product_names:
            inventory_page.add_product_to_cart(name)

        assert inventory_page.get_cart_count() == 3

    @allure.story("Add All Products")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_add_all_products_to_cart(self, inventory_page: InventoryPage):
        """Verify can add all 6 products to cart."""
        for i in range(6):
            inventory_page.add_product_by_index(i)

        assert inventory_page.get_cart_count() == 6

    @allure.story("Cart Badge")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_badge_updates_correctly(self, inventory_page: InventoryPage):
        """Verify cart badge count updates with each add."""
        assert inventory_page.get_cart_count() == 0

        inventory_page.add_product_by_index(0)
        assert inventory_page.get_cart_count() == 1

        inventory_page.add_product_by_index(1)
        assert inventory_page.get_cart_count() == 2


@allure.epic("Shopping Cart")
@allure.feature("Remove from Cart")
class TestRemoveFromCartRegression:
    """Regression tests for remove from cart functionality."""

    @allure.story("Remove Single Product")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_remove_product_from_inventory_page(self, inventory_page: InventoryPage, products: dict):
        """Verify can remove product from cart on inventory page."""
        product_name = products["backpack"]["name"]

        inventory_page.add_product_to_cart(product_name)
        assert inventory_page.get_cart_count() == 1

        inventory_page.remove_product_from_cart(product_name)
        assert inventory_page.get_cart_count() == 0


@allure.epic("Navigation")
@allure.feature("Menu")
class TestMenuNavigationRegression:
    """Regression tests for menu navigation."""

    @allure.story("Menu Operations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_can_open_and_close_menu(self, inventory_page: InventoryPage):
        """Verify menu can be opened and closed."""
        inventory_page.open_menu()
        assert inventory_page.is_menu_open()

        inventory_page.close_menu()
        assert not inventory_page.is_menu_open()

    @allure.story("Reset App State")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_reset_app_state_clears_cart(self, inventory_page: InventoryPage):
        """Verify reset app state clears the cart."""
        inventory_page.add_product_by_index(0)
        inventory_page.add_product_by_index(1)
        assert inventory_page.get_cart_count() == 2

        inventory_page.reset_app_state()

        assert inventory_page.get_cart_count() == 0

    @allure.story("Navigation Links")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_link_navigates_to_cart(self, inventory_page: InventoryPage):
        """Verify cart link navigates to cart page."""
        inventory_page.go_to_cart()

        cart_page = CartPage(inventory_page.page)
        assert cart_page.is_loaded()