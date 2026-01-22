"""Login Regression Test Suite."""

import allure
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@allure.epic("Authentication")
@allure.feature("Login")
class TestLoginRegression:
    """Regression tests for login functionality."""

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_with_standard_user(self, login_page: LoginPage, credentials: dict):
        """Verify standard user can login successfully."""
        login_page.login(credentials["users"]["standard"], credentials["password"])

        inventory = InventoryPage(login_page.page)
        assert inventory.is_loaded(), "Should redirect to inventory page"

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_with_problem_user(self, login_page: LoginPage, credentials: dict):
        """Verify problem user can login."""
        login_page.login(credentials["users"]["problem"], credentials["password"])

        inventory = InventoryPage(login_page.page)
        assert inventory.is_loaded()

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_with_performance_glitch_user(self, login_page: LoginPage, credentials: dict):
        """Verify performance glitch user can login."""
        login_page.login(credentials["users"]["performance"], credentials["password"])

        inventory = InventoryPage(login_page.page)
        assert inventory.is_loaded()

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_with_error_user(self, login_page: LoginPage, credentials: dict):
        """Verify error user can login."""
        login_page.login(credentials["users"]["error"], credentials["password"])

        inventory = InventoryPage(login_page.page)
        assert inventory.is_loaded()

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_with_visual_user(self, login_page: LoginPage, credentials: dict):
        """Verify visual user can login."""
        login_page.login(credentials["users"]["visual"], credentials["password"])

        inventory = InventoryPage(login_page.page)
        assert inventory.is_loaded()

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_fails_with_locked_user(self, login_page: LoginPage, credentials: dict):
        """Verify locked out user cannot login."""
        login_page.login(credentials["users"]["locked"], credentials["password"])

        assert login_page.is_error_displayed()
        assert "locked out" in login_page.get_error_message().lower()

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_login_fails_with_invalid_username(self, login_page: LoginPage, credentials: dict):
        """Verify login fails with non-existent username."""
        login_page.login("invalid_user", credentials["password"])

        assert login_page.is_error_displayed()

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_login_fails_with_wrong_password(self, login_page: LoginPage, credentials: dict):
        """Verify login fails with incorrect password."""
        login_page.login(credentials["users"]["standard"], "wrong_password")

        assert login_page.is_error_displayed()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_fails_with_empty_username(self, login_page: LoginPage, credentials: dict):
        """Verify validation error when username is empty."""
        login_page.enter_password(credentials["password"])
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert "username is required" in login_page.get_error_message().lower()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_fails_with_empty_password(self, login_page: LoginPage, credentials: dict):
        """Verify validation error when password is empty."""
        login_page.enter_username(credentials["users"]["standard"])
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert "password is required" in login_page.get_error_message().lower()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_login_fails_with_empty_credentials(self, login_page: LoginPage):
        """Verify validation error when both fields are empty."""
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert "username is required" in login_page.get_error_message().lower()

    @allure.story("UI Behavior")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_error_message_can_be_dismissed(self, login_page: LoginPage):
        """Verify error message can be closed."""
        login_page.click_login()
        assert login_page.is_error_displayed()

        login_page.close_error()

        assert not login_page.is_error_displayed()

    @allure.story("UI Behavior")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_login_form_elements_are_visible(self, login_page: LoginPage):
        """Verify all login form elements are visible."""
        assert login_page.is_visible(LoginPage.USERNAME_INPUT)
        assert login_page.is_visible(LoginPage.PASSWORD_INPUT)
        assert login_page.is_visible(LoginPage.LOGIN_BUTTON)


@allure.epic("Authentication")
@allure.feature("Logout")
class TestLogoutRegression:
    """Regression tests for logout functionality."""

    @allure.story("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_user_can_logout(self, inventory_page: InventoryPage):
        """Verify user can logout successfully."""
        inventory_page.logout()

        login_page = LoginPage(inventory_page.page)
        assert login_page.is_loaded()

    @allure.story("Session Security")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_cannot_access_inventory_after_logout(self, inventory_page: InventoryPage, settings):
        """Verify inventory is not accessible after logout."""
        inventory_page.logout()
        inventory_page.page.goto(f"{settings.base_url}/inventory.html")

        login_page = LoginPage(inventory_page.page)
        assert login_page.is_loaded()

    @allure.story("Session Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cannot_access_cart_after_logout(self, inventory_page: InventoryPage, settings):
        """Verify cart is not accessible after logout."""
        inventory_page.logout()
        inventory_page.page.goto(f"{settings.base_url}/cart.html")

        login_page = LoginPage(inventory_page.page)
        assert login_page.is_loaded()