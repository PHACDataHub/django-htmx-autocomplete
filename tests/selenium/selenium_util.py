def get_element(driver, selector):
    from selenium.webdriver.common.by import By

    return driver.find_element(By.CSS_SELECTOR, selector)


def get_elements(driver, selector):
    from selenium.webdriver.common.by import By

    return driver.find_elements(By.CSS_SELECTOR, selector)


def click_button(driver, selector):
    # just using element.click() can fail if the element is not in view
    element = get_element(driver, selector)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)


def wait_until_selector(driver, selector):
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(driver, 0.5, poll_frequency=0.1).until(
        expected_conditions.presence_of_element_located(
            ("css selector", selector)
        )
    )


def wait_until_selector_gone(driver, selector):
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(driver, 0.5, poll_frequency=0.1).until_not(
        expected_conditions.presence_of_element_located(
            ("css selector", selector)
        )
    )


def wait_until_stale(driver, element):
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(driver, 0.5, poll_frequency=0.1).until(
        expected_conditions.staleness_of(element)
    )
