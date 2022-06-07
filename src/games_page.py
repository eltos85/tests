import src.decorators
import error_sendler.test_reports
import time
from src.bet_boom_prod import SearchHelper
from src.locators_pc import PcLocators
from error_sendler.websocketlog import WebSocketLogs

locators = PcLocators()
r = error_sendler.test_reports.Report()
wslog = WebSocketLogs()
decorators = src.decorators


class GamesPagesSearchHelper(SearchHelper):

    @decorators.screen
    def click_continue_netent_games(self):
        button = self.find_element(locators.LOCATOR_CONTINUE_BUTTON_IN_GAMES, time=15)
        button.click()

    @src.decorators.time_now("game checker: ")
    @src.decorators._auth
    def game_checker(self, game_config, email, driver=None):
        frames = self.image_list
        try:
            if game_config.get('iframe_1'):
                time.sleep(2)
                self.switch_to_game_frame_1(game_config, frames)
                if game_config.get('iframe_2'):
                    self.switch_to_game_frame_2(game_config, frames)
                if game_config.get('provider') == 'NetEnt':
                    self.click_continue_netent_games()
            self.search_game_locator(game_config, frames)
            if game_config.get('provider_error'):
                self.get_screenshot(frames)
        except Exception as e:
            self.get_screenshot(frames=frames)
            if driver:
                self.game_token = f'{wslog.get_ws_log(driver)}'
            gif = self.add_gif(frames=frames)
            self.send_report(game_config=game_config, gif=gif, e=e, _time=self.time)
            assert False

    @src.decorators.time_now(mess="frame 1")
    @src.decorators.screen
    def switch_to_game_frame_1(self, game_config, frames):
        try:
            time.sleep(game_config.get('sleep'))
            iframe = self.find_element(game_config.get('iframe_game'), game_config.get('timeout_iframe'))
            self.switch_to(iframe)
        except Exception:
            assert False, 'Не смог перейти в первый фрем игры'

    @src.decorators.time_now(mess="frame 2")
    @src.decorators.screen
    def switch_to_game_frame_2(self, game_config, frames):
        try:
            time.sleep(game_config.get('sleep'))
            iframe = self.find_element(game_config.get('iframe_game_2'), game_config.get('timeout_iframe_2'))
            self.switch_to(iframe)
        except Exception:
            assert False, 'Не смог перейти во второй фрем игры'

    @src.decorators.time_now(mess="game locator ")
    @src.decorators.screen
    def search_game_locator(self, game_config, frames):
        try:
            self.find_element(game_config.get('game_locator'), game_config.get('timeout_game'))
        except Exception:
            assert False, 'Игра не открылась'

    def send_report(self, game_config, gif, e, _time):
        if r.get_error_counter() > 0 and r.get_game_name() == game_config.get('game_name'):
            r.add(test_name=f"{game_config.get('test_name')}",
                  type="Game PC",
                  error=e,
                  message=f"{game_config.get('game_name')} :{game_config.get('game_link')}",
                  token=self.game_token,
                  time=_time)
            r.send_message(gif=gif)
            print('error_counter before post message:', r.get_error_counter())
            r.clear_error_counter()
            print('error_counter after post message:', r.get_error_counter())
            r.get_game_name()
        else:
            r.add_game_name(game_config.get('game_name'))
            r.get_game_name()
        r.add_error_counter()

