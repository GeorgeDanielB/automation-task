"""Page Object for the Inventory/Products page."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import allure

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SortOrder(str, Enum):
    """Product sort options."""
    NAME_ASC = "az"
    NAME_DESC = "za"
    PRICE_LOW_HIGH = "lohi"
    PRICE_HIGH_LOW = "hilo"

@dataclass
class ProductInfo:
    """Product information."""
    name: str
    description: str
    price: float

class InventoryPage(BasePage):
    URL_PATH = "/inventory.html"

    # Locators
    APP_LOGO = ".app_logo"
    MENU_BUTTON = "#react-burger-menu-btn"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    MENU_CLOSE_BUTTON = "#react-burger-cross-btn"
    MENU_ALL_ITEMS = "#inventory_sidebar_link"
    MENU_LOGOUT = "#logout_sidebar_link"
    MENU_RESET = "#reset_sidebar_link"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_DESC = ".inventory_item_desc"
    ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "button[id^='add-to-cart']"

    # Navigation

    @allure.step("Open menu")
    def open_menu(self) -> None:
        """Open the hamburger menu."""
        self.click(self.MENU_BUTTON)
        self.wait_for_visible(self.MENU_ALL_ITEMS)

    @allure.step("Close menu")
    def close_menu(self) -> None:
        """Close the hamburger menu."""
        self.click(self.MENU_CLOSE_BUTTON)
        self.wait_for_hidden(self.MENU_ALL_ITEMS)

    @allure.step("Logout")
    def logout(self) -> None:
        """Logout from the application."""
        logger.info("Logging out")
        self.open_menu()
        self.click(self.MENU_LOGOUT)

    @allure.step("Go to cart")
    def go_to_cart(self) -> None:
        """Navigate to the shopping cart."""
        self.click(self.CART_LINK)

    @allure.step("Click on product: {product_name}")
    def click_product(self, product_name: str) -> None:
        """Click on a product to view its details."""
        product_locator = f".inventory_item:has-text('{product_name}') .inventory_item_name"
        self.click(product_locator)

    # Sorting

    @allure.step("Sort products by: {sort_order}")
    def sort_products(self, sort_order: SortOrder) -> None:
        """Sort products by the given order."""
        logger.info(f"Sorting products: {sort_order.value}")
        self.select_option(self.SORT_DROPDOWN, value=sort_order.value)

    # Cart Operations

    @allure.step("Add product to cart: {product_name}")
    def add_product_to_cart(self, product_name: str) -> None:
        """Add a product to the cart by name."""
        logger.info(f"Adding to cart: {product_name}")
        button_id = product_name.lower().replace(" ", "-")
        self.click(f"#add-to-cart-{button_id}")

    @allure.step("Remove product from cart: {product_name}")
    def remove_product_from_cart(self, product_name: str) -> None:
        """Remove a product from the cart by name."""
        logger.info(f"Removing from cart: {product_name}")
        button_id = product_name.lower().replace(" ", "-")
        self.click(f"#remove-{button_id}")

    @allure.step("Add product by index: {index}")
    def add_product_by_index(self, index: int) -> None:
        """Add a product to cart by its position."""
        products = self.page.locator(self.INVENTORY_ITEM)
        add_button = products.nth(index).locator(self.ADD_TO_CART_BUTTON)
        add_button.click()

    def get_cart_count(self) -> int:
        """Get the number of items in the cart."""
        if self.is_visible(self.CART_BADGE):
            count_text = self.get_text(self.CART_BADGE)
            return int(count_text) if count_text else 0
        return 0

    # Product Information

    def get_product_count(self) -> int:
        """Get the number of products displayed."""
        return self.count(self.INVENTORY_ITEM)

    def get_product_names(self) -> List[str]:
        """Get names of all displayed products."""
        return self.get_all_texts(self.ITEM_NAME)

    def get_product_prices(self) -> List[float]:
        """Get prices of all displayed products."""
        price_texts = self.get_all_texts(self.ITEM_PRICE)
        return [float(price.replace("$", "")) for price in price_texts]

    def get_product_info(self, product_name: str) -> Optional[ProductInfo]:
        """Get detailed information about a specific product."""
        product_locator = f".inventory_item:has-text('{product_name}')"
        
        if not self.is_visible(product_locator):
            logger.warning(f"Product not found: {product_name}")
            return None
        
        item = self.page.locator(product_locator)
        name = item.locator(self.ITEM_NAME).text_content()
        description = item.locator(self.ITEM_DESC).text_content()
        price_text = item.locator(self.ITEM_PRICE).text_content()
        price = float(price_text.replace("$", ""))

        return ProductInfo(name=name, description=description, price=price)

    def get_all_products(self) -> List[ProductInfo]:
        """Get information about all displayed products."""
        products = []
        for name in self.get_product_names():
            info = self.get_product_info(name)
            if info:
                products.append(info)
        return products

    # Validations

    @allure.step("Verify page is loaded")
    def is_loaded(self) -> bool:
        """Verify the inventory page is fully loaded."""
        return (
            self.is_visible(self.INVENTORY_LIST) and
            self.is_visible(self.APP_LOGO) and
            self.get_product_count() > 0
        )

    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if a product has been added to the cart."""
        button_id = product_name.lower().replace(" ", "-")
        return self.is_visible(f"#remove-{button_id}")

    def is_menu_open(self) -> bool:
        """Check if the hamburger menu is open."""
        return self.is_visible(self.MENU_ALL_ITEMS)

    def reset_app_state(self) -> None:
        """Reset the application state via menu option."""
        logger.info("Resetting application state")
        self.open_menu()
        self.click(self.MENU_RESET)
        self.close_menu()
