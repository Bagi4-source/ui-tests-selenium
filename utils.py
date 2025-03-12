import random
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def click(driver, element):
    driver.execute_script("arguments[0].click();", element)


def wait_for_element(driver, by: By, locator: str, timeout: int = 10):
    """
    Ждет, пока элемент с заданным локатором появится в DOM
    :param driver: Экземпляр WebDriver
    :param by: Тип локатора (например, By.XPATH, By.CSS_SELECTOR)
    :param locator: Строка локатора
    :param timeout: Таймаут ожидания в секундах
    """
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))


def wait_for_dom_content_loaded(driver, timeout: int = 10):
    """
    Ждет, пока DOM перейдет в состояние 'interactive' или 'complete'
    :param driver: Экземпляр WebDriver
    :param timeout: Таймаут ожидания в секундах
    """
    end_time = time.time() + timeout
    while True:
        ready_state = driver.execute_script("return document.readyState;")
        if ready_state in ["interactive", "complete"]:
            break
        if time.time() > end_time:
            raise TimeoutError("Ожидание DOMContentLoaded превысило заданный таймаут.")
        time.sleep(0.2)


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def send_keys(el, text):
    for symbol in text:
        el.send_keys(symbol)
        time.sleep(random.randint(4, 9) * 0.01)
