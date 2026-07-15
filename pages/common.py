"""Shared helpers for SauceDemo page objects."""


def product_slug(product_name: str) -> str:
    return product_name.lower().replace(" ", "-")


def add_to_cart_selector(product_name: str) -> str:
    return f"[data-test='add-to-cart-{product_slug(product_name)}']"


def remove_from_cart_selector(product_name: str) -> str:
    return f"[data-test='remove-{product_slug(product_name)}']"
