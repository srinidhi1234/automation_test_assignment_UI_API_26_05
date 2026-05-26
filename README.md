# automation_test_assignment_UI_API_26_05

This project contains pytest API tests for JSONPlaceholder/httpbin and Playwright UI tests for Sauce Demo.

## Install

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run

```bash
pytest
```

The tests are written to run independently from the project root. UI setup is handled by pytest fixtures and the `pytest-playwright` plugin.
