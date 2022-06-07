import json
import argparse
import re
import requests

parser = argparse.ArgumentParser(description='Parser for allure report')
parser.add_argument('--test_cases_dir', required=True, type=str, help='Test cases directory path')
parser.add_argument('--categories_file', required=True, type=str, help='categories.json file path')
parser.add_argument('test_name', type=str, help='Test name')
args = parser.parse_args()

test_cases_dir = args.test_cases_dir
categories_file = args.categories_file
test_name = args.test_name


def send_message(error_message):
    requests.post('http://127.0.0.1:5000/', json=error_message)


def search_file(test_cases_dir, uid):
    message = {'test_name': test_name}
    arr_linc = []
    for i in uid:
        file = test_cases_dir + '/' + i + '.json'
        with open(file, 'r') as f:
            linc_game = json.load(f)
            arr_linc.append(json.dumps(linc_game['testStage']['steps'][0]['name'], ensure_ascii=False, indent=4))

    for i in arr_linc:
        found_links = re.findall('https?://[a-zA-Z0-9-\.\/-]*', i)
        case_link = 'NO'
        if len(found_links) > 0:
            case_link = found_links[0]
        message[str(re.sub('[^\x00-\x7f]|(?P<url>https?://[^\s]+)|"| ', '', i))] = case_link
    send_message(message)
    print(message)

def search_uid_categories_json(cat_file):
    arr_categories = []
    uid = []
    with open(cat_file, 'r') as f:
        data = json.load(f)
    for index in data['children'][0]['children'][0]:
        if index == 'children':
            arr_categories = data['children'][0]['children'][0][index]
    for index in range(len(arr_categories)):
        s = arr_categories[index]
        uid.append(s['uid'])
    return uid


search_file(test_cases_dir, search_uid_categories_json(categories_file))
