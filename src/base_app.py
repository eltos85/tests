# Базовые функции
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from faker import Faker
import os
import configparser
from PIL import Image
from io import BytesIO
import error_sendler.test_reports

r = error_sendler.test_reports.Report()


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'conf.cfg'))
        self.errors_file = dict()

        # тестовое окружение
        self.uk_user_prod = self.config.get('user', 'uk_prod_user')
        self.ge_user_prod = self.config.get('user', 'ge_prod_user')
        self.bl_user_prod = self.config.get('user', 'bl_prod_user')
        self.de_user_prod = self.config.get('user', 'de_prod_user')
        # продовое окружение
        self.prod_user_mail = self.config.get('user', 'prod_user_mail')
        self.prod_user_password = self.config.get('user', 'prod_user_password')
        self.random_mail = Faker().user_name() + '@test.test'
        self.payment_page = self.config.get('url', 'payment_page')
        self.image_list = []
        self.game_token = ""
        self.time = []
        self.gif = 'png_to_gif.gif'

    def find_element(self, locator, time=150):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=15):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def switch_to(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.frame_to_be_available_and_switch_to_it(locator),
                                                      message=f"Can't find elements by locator {locator}")

    # дожидается пока элемент не станет кликабельным

    def find_element_clickable(self, locator, time=15):
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator),
                                                      message=f"Can't find element by locator {locator}")

    def get_user(self, country):
        if country == "UA":
            return self.uk_user_prod
        elif country == "BL":
            return self.bl_user_prod
        elif country == "GE":
            return self.ge_user_prod
        elif country == "DE":
            return self.de_user_prod
        else:
            return self.prod_user_mail

    def get_screenshot(self, frames):
        frames.append(Image.open(BytesIO(self.driver.get_screenshot_as_png())))
        return frames

    def add_gif(self, frames):
        frames[0].save(self.gif,
                       save_all=True,
                       append_images=frames[1:],
                       optimize=True,
                       duration=500,
                       loop=0
                       )
        self.gif = open('png_to_gif.gif', 'rb')
        return self.gif

    def refresh(self):
        self.driver.refresh()


    def send_keys_workaround(self, element, string):
        for s in string:
            if s == '1':
                element.send_keys(Keys.NUMPAD1)
            elif s == '2':
                element.send_keys(Keys.NUMPAD2)
            elif s == '3':
                element.send_keys(Keys.NUMPAD3)
            elif s == '4':
                element.send_keys(Keys.NUMPAD4)
            elif s == '5':
                element.send_keys(Keys.NUMPAD5)
            elif s == '6':
                element.send_keys(Keys.NUMPAD6)
            elif s == '7':
                element.send_keys(Keys.NUMPAD7)
            elif s == '8':
                element.send_keys(Keys.NUMPAD8)
            elif s == '9':
                element.send_keys(Keys.NUMPAD9)
            elif s == '0':
                element.send_keys(Keys.NUMPAD0)
            else:
                element.send_keys(s)

    def base_reporter(self, provider, provider_method, error, gif):
        rerun = r.get_error_counter()
        if rerun > 0:
            r.add(test_name=provider,
                  Type=provider_method,
                  message=f"Error:{error}")
            r.send_message(gif=gif)
            r.clear_error_counter()
            r.get_game_name()
        else:
            r.add_game_name(provider)
            r.get_game_name()
        r.add_error_counter()
