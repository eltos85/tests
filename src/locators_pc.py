from selenium.webdriver.common.by import By


class PcLocators:
    LOCATOR_CLOSE_REG_MODAL = (By.XPATH, '//button[@form="authRegForm"]')
    # Локаторы для netent
    LOCATOR_CONTINUE_BUTTON_IN_GAMES = (By.TAG_NAME, 'undefined')
    # Кнопка завершения регистрации
    LOCATOR_COMPLETE_REG_AUTH_BUTTON = (By.XPATH, '//button[contains(@class, "_auth-reg_sumbitButton")]')

    # Выбор авторизации по емаилу в окне авторизации
    LOCATOR_CHOICE_EMAIL_AUTH = (By.XPATH, '//div[@data-at="tab-auth-email"]')
    LOCATOR_INPUT_EMAIL = (By.NAME, 'email')
    LOCATOR_INPUT_PASSWORD = (By.NAME, 'password')

    # Поп-ап регистрации
    LOCATOR_LOG_IN = (By.XPATH, '//a[contains(@href, "modal")]')

    # Cookies
    LOCATOR_NOTIFICATION_FORM_ACCESS = (By.ID, 'onesignal-slidedown-cancel-button')

