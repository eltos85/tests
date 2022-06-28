# Подключение вебдрайвера
import pytest
from selenium import webdriver
from src.bet_boom_prod import SearchHelper
from src.games_page import GamesPagesSearchHelper


@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
    chrm_caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    # driver = webdriver.Chrome(options=options, desired_capabilities=chrm_caps)
    driver = webdriver.Remote("http://selenium:4444/wd/hub", options=options,
                              desired_capabilities=chrm_caps)
    driver.implicitly_wait(10)
    driver.set_window_size(1600, 1000)
    yield driver
    driver.quit()


@pytest.fixture()
def page(browser):
    yield SearchHelper(browser)


@pytest.fixture()
def game(browser):
    yield GamesPagesSearchHelper(browser)


def pytest_addoption(parser):
    parser.addoption("--country", action="store")
    parser.addoption("--provider", action="store")


@pytest.fixture(scope='session')
def country(request):
    return request.config.option.country

@pytest.fixture(scope='session')
def provider(request):
    return request.config.option.provider

