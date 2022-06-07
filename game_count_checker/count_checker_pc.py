import json
from websocket import create_connection
import websocket
import const_file
import configparser
import sys

country = sys.argv[1]
game_config = sys.argv[2]

config = configparser.ConfigParser()

config.read(rf'{game_config}')
websocket.enableTrace(True)
ws = create_connection(const_file.WS_URL)
dict_games_page = [const_file.TOP_GAMES, const_file.NEW_GAMES, const_file.RECOMMENDED_GAMES]
games_list = []
games_id_list = {}
games_id = {}
a = []
b = []
for get_games in dict_games_page:
    ws.send(get_games)
    result = ws.recv()

    j = json.loads(format(result))
    for i in j['result']['games']:
        games_list.append(i['label'])
        games_id_list[str(i['label']).lower()] = int(i['pageId'])

games_config = list(map(lambda x: x.lower(), config.options("Games")))
games_prod = list(map(lambda x: x.lower(), games_list))
prod_list = list(set(games_prod) - set(games_config))
conf_list = list(set(games_config) - set(games_prod))

for i in prod_list:
    if i is not games_id_list.keys():
        j = i + " : " + f"https://bet-boom.com/{country}/game/{games_id_list[i]}/"
        a.append(j)
print("Количество игр на главной: ", len(games_prod))
print(f'Игры для замены {a}')
print('Разность конфига с реальным списком: ', list(set(games_config) - set(games_prod)))

