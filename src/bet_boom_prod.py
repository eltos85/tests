# Главная страница продвого сайта
from src.base_app import BasePage
import error_sendler.test_reports
from src.locators_pc import PcLocators

locators = PcLocators()
r = error_sendler.test_reports.Report()


class SearchHelper(BasePage):

    def choice_email_login_auth(self):
        try:
            choice_email_login = self.find_element_clickable(locators.LOCATOR_CHOICE_EMAIL_AUTH, time=10)
            return choice_email_login.click()
        except Exception:
            assert False, 'Не удалось переключить на регу по почте'

    def prod_email_login(self, login):
        input_login = self.find_element(locators.LOCATOR_INPUT_EMAIL, time=15)
        assert input_login, 'check login input error'
        # input_login.click()
        return input_login.send_keys(login)

    def enter_prod_password(self):  # Ввод пароля пользователя
        try:
            password = self.find_element(locators.LOCATOR_INPUT_PASSWORD)
            password.send_keys(self.prod_user_password)
        except:
            assert False

    # Нажатие кнопки "Логин" в форме авторизации
    def click_auth_button(self):
        try:
            click_auth_button_en = self.find_element_clickable(locators.LOCATOR_COMPLETE_REG_AUTH_BUTTON,
                                                               time=2)
            click_auth_button_en.click()
        except Exception:
            assert False, 'Кнопка завершения авторизации не сработала'

    def auth(self, email):
        page = SearchHelper
        login = self.find_element(locators.LOCATOR_LOG_IN)
        self.driver.execute_script("arguments[0].click();", login)
        page.choice_email_login_auth(self)
        page.prod_email_login(self, email)
        page.enter_prod_password(self)
        page.click_auth_button(self)
        print("Авторизация прошла успешно")

    def check_notification_access_message(self):
        try:
            self.find_element(locators.LOCATOR_NOTIFICATION_FORM_ACCESS, 10).click()
        except Exception:
            return True

