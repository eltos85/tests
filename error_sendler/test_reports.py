import re
import telebot
from jinja2 import Template
from error_sendler import const
import logging

loc_bot = const
token = loc_bot.Locators.TOKEN
chat_id = loc_bot.Locators.CHAT_ID_PROD
chat_id_pay = loc_bot.Locators.CHAT_ID_PAY
bot = telebot.TeleBot(token)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(massage)s',
                    level=logging.INFO,
                    filename='bot.log')


class Report:
    def __init__(self):
        self.report = dict()
        self.text = dict()
        self.index = 1
        self.error_counter = 0
        self.game_name = ""

    def add_error_counter(self):
        self.error_counter = 1

    def add_game_name(self, game):
        print('add game name: ' + game)
        self.game_name = f"{game}"

    def get_game_name(self):
        print("game name: " + self.game_name)
        return self.game_name

    def clear_error_counter(self):
        self.error_counter = 0

    def add(self, test_name, message, **additional):
        self.report = dict(test_name=test_name, **additional)
        mes = re.sub(r'[()\[|\]\',]', '', str(message))
        self.text[f"{self.index}"] = f"{mes}"
        if mes is not self.report:
            self.report['Error'] = '\n   💩' + '\n   💩'.join([f':{self.text[i]}' for i in self.text])
        self.index += 1
        return self

    def get_error_counter(self):
        return self.error_counter

    def send_message(self, gif=None, img=None):
        logging.info('Send message')
        template = """
                **{{ data['test_name'].replace('_', ' ') }}**☠☠☠
                \n{% for case_name in data if case_name != 'test_name' %} {{ case_name }}: {{ data[case_name] }}\n{% endfor %}
                """
        template = Template(template)
        template = template.render(data=self.report, dttm=template)
        if gif is not None:
            bot.send_animation(chat_id, gif, caption=template)
        elif img is not None:
            bot.send_photo(chat_id, img, caption=template)
        else:
            bot.send_message(chat_id, template)
        self.text.clear()
