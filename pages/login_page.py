"""Page Object for the Login page."""

import allure

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    URL_PATH = ""

    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"
    LOGO = ".login_logo"

    # Actions

    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str) -> None:
        """Perform login with given credentials."""
        logger.info(f"Attempting login with username: {username}")

        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

        logger.info("Login form submitted")

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str) -> None:
        """Enter username only."""
        self.fill(self.USERNAME_INPUT, username)

    @allure.step("Enter password")
    def enter_password(self, password: str) -> None:
        """Enter password only."""
        self.fill(self.PASSWORD_INPUT, password)

    @allure.step("Click login button")
    def click_login(self) -> None:
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Close error message")
    def close_error(self) -> None:
        """Close the error message by clicking the X button."""
        if self.is_error_displayed():
            self.click(self.ERROR_BUTTON)
            logger.debug("Closed error message")

    # Getters

    def get_error_message(self) -> str:
        """Get the current error message text."""
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    # Validations

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed."""
        return self.is_visible(self.ERROR_MESSAGE)

    @allure.step("Verify page is loaded")
    def is_loaded(self) -> bool:
        """Verify the login page is fully loaded."""
        return (
            self.is_visible(self.USERNAME_INPUT) and
            self.is_visible(self.PASSWORD_INPUT) and
            self.is_visible(self.LOGIN_BUTTON)
        )