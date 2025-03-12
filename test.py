import hashlib
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils import wait_for_dom_content_loaded, wait_for_element, click, scroll_into_view, send_keys


class MyTestCase(unittest.TestCase):
    driver = webdriver.Chrome(Options(), service=Service('./chromedriver.exe'))
    actions = webdriver.ActionChains(driver)

    @classmethod
    def setUpClass(cls):
        cls.driver.set_window_size(1200, 800)

    def __init_page(self):
        self.driver.get('https://fktpm.k-lab.su/ru')
        wait_for_dom_content_loaded(self.driver)
        time.sleep(1)

    def test_click_on_abiturient(self):
        self.__init_page()
        wait_for_element(driver=self.driver, locator='//a[@href="/abiturient"]', by=By.XPATH)
        abit_links = self.driver.find_elements(value='//a[@href="/abiturient"]', by=By.XPATH)
        if abit_links:
            self.actions.move_to_element(abit_links[0])
            click(self.driver, abit_links[0])
            time.sleep(1)
            wait_for_dom_content_loaded(self.driver)
        self.assertTrue(self.driver.current_url.endswith("/abiturient"))

    def test_hash_of_main_page(self):
        self.__init_page()
        screenshot = self.driver.get_screenshot_as_base64()
        result = hashlib.sha256(screenshot.encode('utf-8')).hexdigest()
        self.assertEqual("46a0194d6d53068fd8e7a2fffc74cdafc8dc067bebea9494d21750f2c852ebef", result)

    def __set_data_to_form(self, form_data: dict) -> str:
        self.__init_page()
        wait_for_element(driver=self.driver, locator='//input[@name="name"]', by=By.XPATH)
        name_input = self.driver.find_element(value='//input[@name="name"]', by=By.XPATH)
        phone_input = self.driver.find_element(value='//input[@name="phone"]', by=By.XPATH)
        email_input = self.driver.find_element(value='//input[@name="email"]', by=By.XPATH)

        wrapper: WebElement = self.driver.execute_script(
            "return arguments[0].parentNode.parentNode.parentNode.parentNode.parentNode;", name_input)

        send_keys(name_input, form_data["name"])
        send_keys(phone_input, form_data["phone"])
        send_keys(email_input, form_data["email"])
        time.sleep(0.5)

        screenshot = wrapper.screenshot_as_base64
        return hashlib.sha256(screenshot.encode('utf-8')).hexdigest()

    def test_form_validation_valid(self):
        mock_data = {
            "name": "Герман",
            "email": "nigga@mail.ru",
            "phone": "+79181234567"
        }
        result = self.__set_data_to_form(mock_data)
        self.assertEqual("4ca534b58950e549c5144717b46f2a64183709ea55c53f15b4743e4e56f23975", result)

    def test_form_validation_invalid(self):
        mock_data = {
            "name": "Герман",
            "email": "nigga@mail.ru",
            "phone": "2222"
        }
        result = self.__set_data_to_form(mock_data)
        self.assertEqual("d894a7b11eeba1731b68e3e9d9b0b071ca8f7eeae4e2cb483dfdd534bda945dc", result)

        mock_data = {
            "name": "",
            "email": "nigga@mail.ru",
            "phone": "2222"
        }
        result = self.__set_data_to_form(mock_data)
        self.assertEqual("0dbb5dff07c212c3a8c44a6d29c41c52e94fa846d4e4e1f9d688db106b9b9995", result)

        mock_data = {
            "name": "",
            "email": "error",
            "phone": "2222"
        }
        result = self.__set_data_to_form(mock_data)
        self.assertEqual("6ae1afc37e417441a8335c9b988743a4129b11c6861ba52338d5c761402ed34f", result)


if __name__ == '__main__':
    unittest.main()
