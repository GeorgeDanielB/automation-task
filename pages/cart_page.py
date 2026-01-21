"""Page Object for the Shopping Cart page."""

from dataclasses import dataclass
from typing import List, Optional

import allure

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CartItem:
    """Cart item information."""
    name: str
    description: str
    price: float
    quantity: int = 1


class CartPage(BasePage):
    URL_PATH = "/cart.html"
    PAGE_TITLE = "Swag Labs"

    # Locators
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    ITEM_QUANTITY = ".cart_quantity"
    ITEM_NAME = ".inventory_item_name"
    ITEM_DESC = ".inventory_item_desc"
    ITEM_PRICE = ".inventory_item_price"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"
    CHECKOUT_BUTTON = "#checkout"

    # Navigation

    @allure.step("Continue shopping")
    def continue_shopping(self) -> None:
        """Return to the inventory page."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self) -> None:
        """Proceed to the checkout page."""
        logger.info("Proceeding to checkout")
        self.click(self.CHECKOUT_BUTTON)

    # Cart Operations

    @allure.step("Remove item: {item_name}")
    def remove_item(self, item_name: str) -> None:
        """Remove an item from the cart by name."""
        logger.info(f"Removing item from cart: {item_name}")
        button_id = item_name.lower().replace(" ", "-")
        self.click(f"#remove-{button_id}")

    # Getters

    def get_item_count(self) -> int:
        """Get the number of items in the cart."""
        return self.count(self.CART_ITEM)

    def get_item_names(self) -> List[str]:
        """Get names of all items in the cart."""
        return self.get_all_texts(self.ITEM_NAME)

    def get_item_prices(self) -> List[float]:
        """Get prices of all items in the cart."""
        price_texts = self.get_all_texts(self.ITEM_PRICE)
        return [float(price.replace("$", "")) for price in price_texts]

    def get_cart_item(self, item_name: str) -> Optional[CartItem]:
        """Get details of a specific cart item."""
        item_locator = f".cart_item:has-text('{item_name}')"

        if not self.is_visible(item_locator):
            return None

        item = self.page.locator(item_locator)
        return CartItem(
            name=item.locator(self.ITEM_NAME).text_content(),
            description=item.locator(self.ITEM_DESC).text_content(),
            price=float(item.locator(self.ITEM_PRICE).text_content().replace("$", "")),
            quantity=int(item.locator(self.ITEM_QUANTITY).text_content()),
        )

    # Validations

    @allure.step("Verify page is loaded")
    def is_loaded(self) -> bool:
        """Verify the cart page is fully loaded."""
        return (
            self.is_visible(self.CART_LIST) and
            self.is_visible(self.CHECKOUT_BUTTON) and
            self.is_visible(self.CONTINUE_SHOPPING_BUTTON)
        )

    def is_empty(self) -> bool:
        """Check if the cart is empty."""
        return self.get_item_count() == 0

    def contains_item(self, item_name: str) -> bool:
        """Check if a specific item is in the cart."""
        return item_name in self.get_item_names()
