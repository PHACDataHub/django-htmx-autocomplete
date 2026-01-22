import pytest


# override the global autouse fixture just for selenium tests in this package
# see tests/conftest.py's enable_db_access_for_all_tests
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


@pytest.fixture(scope="session")
def driver():
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()
