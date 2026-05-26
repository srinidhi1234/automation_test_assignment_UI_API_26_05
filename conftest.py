from dataclasses import dataclass

import pytest
import requests
from playwright.sync_api import Page, expect


JSONPLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"
HTTPBIN_BASE_URL = "https://httpbin.org"
SAUCEDEMO_BASE_URL = "https://www.saucedemo.com"


@dataclass(frozen=True)
class SauceUser:
    username: str
    password: str = "secret_sauce"


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session


@pytest.fixture(scope="session")
def jsonplaceholder_base_url() -> str:
    return JSONPLACEHOLDER_BASE_URL


@pytest.fixture(scope="session")
def httpbin_base_url() -> str:
    return HTTPBIN_BASE_URL


@pytest.fixture
def standard_user() -> SauceUser:
    return SauceUser(username="standard_user")


@pytest.fixture
def locked_out_user() -> SauceUser:
    return SauceUser(username="locked_out_user")


@pytest.fixture
def problem_user() -> SauceUser:
    return SauceUser(username="problem_user")


@pytest.fixture
def login_page(page: Page) -> Page:
    page.goto(SAUCEDEMO_BASE_URL)
    expect(page.locator("[data-test='login-button']")).to_be_visible()
    return page


@pytest.fixture
def login_as(login_page: Page):
    def _login(user: SauceUser, password: str | None = None) -> Page:
        login_page.locator("[data-test='username']").fill(user.username)
        login_page.locator("[data-test='password']").fill(
            user.password if password is None else password
        )
        login_page.locator("[data-test='login-button']").click()
        return login_page

    return _login


@pytest.fixture
def inventory_page(login_as, standard_user: SauceUser) -> Page:
    page = login_as(standard_user)
    expect(page).to_have_url(f"{SAUCEDEMO_BASE_URL}/inventory.html")
    expect(page.locator("[data-test='inventory-item']")).to_have_count(6)
    return page
