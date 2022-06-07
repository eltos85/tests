import datetime
from PIL import Image
from io import BytesIO
from src.locators_pc import PcLocators
from selenium.common.exceptions import TimeoutException

locators = PcLocators()


def time_now(mess):
    def _time_now(func):
        def get_time_now(*args, **kwargs):
            began = datetime.datetime.now()
            func(*args, **kwargs)
            __time = mess + f"{datetime.datetime.now() - began}"
            args[0].time.append(__time)
            print(__time)
        return get_time_now

    return _time_now


def screen(func):
    def _screen(*args, **kwargs):
        args[0].image_list.append(Image.open(BytesIO(args[0].driver.get_screenshot_as_png())))
        func(*args, **kwargs)
        args[0].image_list.append(Image.open(BytesIO(args[0].driver.get_screenshot_as_png())))
    return _screen


def _auth(fanc):
    def try_auth(*args, **kwargs):
        try:
            args[0].image_list.append(Image.open(BytesIO(args[0].driver.get_screenshot_as_png())))
            args[0].find_element(locators.LOCATOR_CLOSE_REG_MODAL, time=15)
            args[0].auth(kwargs['email'])
            args[0].check_notification_access_message()
            args[0].image_list.append(Image.open(BytesIO(args[0].driver.get_screenshot_as_png())))
            fanc(*args, **kwargs)
        except TimeoutException:
            return True
    return try_auth