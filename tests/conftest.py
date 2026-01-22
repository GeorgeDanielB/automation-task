"""Pytest Configuration and Fixtures."""

import os
from datetime import datetime
from pathlib import Path
from typing import Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.settings import BrowserType, Settings, get_settings
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.file_handler import FileHandler
from utils.logger import TestContextFilter, get_logger, setup_logging

logger = get_logger(__name__)


# Command Line Options

def pytest_addoption(parser):
    parser.addoption("--headless", default="true", choices=["true", "false"])
    parser.addoption("--slow-mo", default="0")


# Pytest Hooks

def pytest_configure(config):
    setup_logging()
    Path("reports").mkdir(exist_ok=True)
    Path("screenshots").mkdir(exist_ok=True)


def pytest_runtest_setup(item):
    TestContextFilter.set_current_test(item.name)
    logger.info(f"Starting test: {item.name}")


def pytest_runtest_teardown(item):
    logger.info(f"Finished test: {item.name}")
    TestContextFilter.set_current_test(None)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshots/{item.name}_{timestamp}.png"
                page.screenshot(path=screenshot_path)
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=f"Failure Screenshot - {item.name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
            except Exception as e:
                logger.warning(f"Failed to capture screenshot: {e}")


# Settings Fixture

@pytest.fixture(scope="session")
def settings(request) -> Settings:
    browser = request.config.getoption("--browser", default="chromium")
    if isinstance(browser, list):
        browser = browser[0] if browser else "chromium"

    headless = request.config.getoption("--headless") == "true"
    slow_mo = int(request.config.getoption("--slow-mo"))

    os.environ["BROWSER"] = str(browser)
    os.environ["HEADLESS"] = str(headless).lower()
    os.environ["SLOW_MO"] = str(slow_mo)

    get_settings.cache_clear()
    return get_settings()


# Browser Fixtures

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Generator[Browser, None, None]:
    browser_launcher = {
        BrowserType.CHROMIUM: playwright_instance.chromium,
        BrowserType.FIREFOX: playwright_instance.firefox,
        BrowserType.WEBKIT: playwright_instance.webkit,
    }[settings.browser]

    launch_options = {"headless": settings.headless, "slow_mo": settings.slow_mo}
    if settings.browser == BrowserType.CHROMIUM:
        launch_options["args"] = ["--no-sandbox", "--disable-dev-shm-usage"]

    browser = browser_launcher.launch(**launch_options)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser, settings: Settings) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(
        viewport={"width": settings.viewport_width, "height": settings.viewport_height},
        ignore_https_errors=True,
    )
    context.set_default_timeout(settings.default_timeout)
    context.set_default_navigation_timeout(settings.navigation_timeout)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page
    page.close()


# Data Fixtures

@pytest.fixture
def test_data() -> dict:
    data_file = Path("data/test_data.yaml")
    if data_file.exists():
        return FileHandler().read_yaml(data_file)
    return {}


@pytest.fixture
def credentials(test_data: dict) -> dict:
    return test_data.get("credentials", {})


@pytest.fixture
def products(test_data: dict) -> dict:
    return test_data.get("products", {})


@pytest.fixture
def checkout_data(test_data: dict) -> dict:
    return test_data.get("checkout", {})


# Page Object Fixtures

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.navigate()
    return login


@pytest.fixture
def inventory_page(page: Page, test_data: dict) -> InventoryPage:
    creds = test_data.get("credentials", {})
    login = LoginPage(page)
    login.navigate()
    login.login(creds["users"]["standard"], creds["password"])

    inventory = InventoryPage(page)
    inventory.wait_for_load_state("networkidle")
    return inventory


@pytest.fixture
def cart_page(inventory_page: InventoryPage) -> CartPage:
    inventory_page.go_to_cart()
    return CartPage(inventory_page.page)


@pytest.fixture
def checkout_page(inventory_page: InventoryPage) -> CheckoutPage:
    inventory_page.add_product_by_index(0)
    inventory_page.go_to_cart()
    cart = CartPage(inventory_page.page)
    cart.proceed_to_checkout()
    return CheckoutPage(inventory_page.page)