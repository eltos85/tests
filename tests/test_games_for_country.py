import pytest
import yaml
conf = open("configs/test.yaml")
yaml_conf = yaml.safe_load(conf)


@pytest.mark.parametrize('games', [i for i in yaml_conf])
def test_game(country, games, game, browser):
    browser.get(yaml_conf.get(games).get('game_link'))
    game.game_checker(yaml_conf.get(games), email=game.prod_user_mail, driver=browser)