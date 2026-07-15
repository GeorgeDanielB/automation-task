# Automation task

Test automation framework for SauceDemo (https://www.saucedemo.com) built with Python, Playwright, and Pytest.

## Structure

```
automation-task/
├── config/
│   └── settings.py          # Configuration management (pydantic-settings, .env support)
├── core/
│   ├── base_page.py         # Base class for all page objects
│   └── element_handler.py   # Wrapper for element interactions (logging + failure screenshots)
├── pages/
│   ├── common.py            # Shared selector helpers
│   ├── login_page.py        # Login page object
│   ├── inventory_page.py    # Products page object
│   ├── cart_page.py         # Cart page object
│   └── checkout_page.py     # Checkout page object
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
├── .env.example             # Configuration template
└── .github/workflows/ci.yml # CI pipeline (lint + smoke + regression)
```

## Setup

Requires Python 3.11+.

```bash
# Navigate to project folder (where you extracted the files)
cd <project-folder>

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Configuration

Defaults work out of the box. To override, copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | https://www.saucedemo.com | Target application |
| `BROWSER` | chromium | chromium / firefox / webkit |
| `HEADLESS` | true | Run without visible browser |
| `SLOW_MO` | 0 | Delay between actions (ms) |
| `DEFAULT_TIMEOUT` | 30000 | Element timeout (ms) |
| `NAVIGATION_TIMEOUT` | 60000 | Page navigation timeout (ms) |

CLI options (`--browser`, `--headless`, `--slow-mo`) take precedence over `.env`.

## Running Tests

```bash
# Smoke tests
pytest -m smoke

# Full regression
pytest -m regression

# Parallel execution (pytest-xdist)
pytest -m regression -n auto

# Visible browser
pytest -m smoke --headless=false

# Specific browser
pytest --browser=firefox

# Slow motion for debugging
pytest -m smoke --headless=false --slow-mo=500

# Single file
pytest tests/test_login.py
```

## Reports

- Logs are written to `reports/test_run_<date>.log`
- Screenshots are captured automatically on failure in `screenshots/`

Allure report:
```bash
brew install allure
pytest -m regression --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Code Quality

```bash
ruff check .        # lint
ruff check . --fix  # auto-fix
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

GitHub Actions (`.github/workflows/ci.yml`):
- Every push/PR: ruff lint, then smoke tests on Chromium
- Manual trigger: full regression in parallel on Chromium, Firefox, and WebKit
- Allure results uploaded as artifacts; screenshots and logs uploaded on failure
