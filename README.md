# Automation task

Test automation framework for SauceDemo (https://www.saucedemo.com) built with Python, Playwright, and Pytest.

## Structure

```
automation-task/
├── config/
│   └── settings.py          # Configuration management
├── core/
│   ├── base_page.py         # Base class for all page objects
│   └── element_handler.py   # Wrapper for element interactions
├── pages/
│   ├── login_page.py        # Login page object
│   ├── inventory_page.py    # Products page object
│   ├── cart_page.py         # Cart page object
│   ├── checkout_page.py     # Checkout page object
├── tests/
│   ├── conftest.py          # Pytest fixtures and hooks
│   ├── test_login.py        # Login and logout tests
│   ├── test_inventory.py    # Product catalog tests
│   ├── test_cart.py         # Shopping cart tests
│   └── test_checkout.py     # Checkout flow tests
├── utils/
│   ├── logger.py            # Logging configuration
│   └── file_handler.py      # YAML file reader for test data
├── data/
│   └── test_data.yaml       # Test data (credentials, products)
└── .github/workflows/ci.yml # CI pipeline
```

## Setup

```bash
# Navigate to project folder (where you extracted the files)
cd <project-folder>

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Running Tests

```bash
# Smoke tests
pytest -m smoke

# Full regression
pytest -m regression

# Visible browser
pytest -m smoke --headless=false

# Specific browser
pytest --browser=firefox

# Single file
pytest tests/test_login.py
```

## Reports

Allure report:
```bash
brew install allure
pytest -m regression --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Test Coverage

- Login: 13 tests
- Logout: 3 tests
- Inventory: 16 tests
- Cart: 8 tests
- Checkout: 12 tests
- Total: 52 tests

## Test Users

- standard_user - happy path
- locked_out_user - locked account
- problem_user - has bugs
- performance_glitch_user - slow responses
- error_user - triggers errors
- visual_user - visual bugs

Password for all: secret_sauce

## CI/CD

GitHub Actions:
- Push/PR: runs smoke tests
- Manual trigger: runs full regression on all browsers
