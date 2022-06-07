import json


class WebSocketLogs:

    def get_ws_log(self, driver):
        global result
        dict_response = []
        for wsData in driver.get_log('performance'):
            wsJson = json.loads((wsData["message"]))
            if wsJson["message"]["method"] == "Network.webSocketFrameReceived":
                get_response = (wsJson["message"]["params"]["response"][
                    "payloadData"])
                if 'callBilling' in get_response:
                    dict_response.append(get_response)
        list_response = list(map(lambda x: x, dict_response))
        for index_json in range(len(list_response)):
            token_game = json.loads(list_response[index_json])
            try:
                if token_game['method'] == 'getToken':
                    result = token_game['result']['token']
                elif token_game['method'] == 'getTokenDemo':
                    result = token_game['result']['token']
                return result
            except Exception:
                assert True

