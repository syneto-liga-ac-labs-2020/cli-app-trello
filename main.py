import argparse
import os
import requests
from pprint import pprint

def get_auth(filepath):
    with open(filepath,'r') as f:
        contents = f.readlines()
        return contents[0].strip('\n'),contents[1].strip('\n')
    return ("","")

def get_user_boards(key, token):
    url = f'https://api.trello.com/1/members/me/boards?key={key}&token={token}'
    response = requests.get(url)
    result = []
    for board in response.json():
        result.append({'id':board.get('id'), 'name':board.get('name')})

    return result

def get_user_lists(key,token,board_id):
    url= f"https://api.trello.com/1/boards/{board_id}/lists?key={key}&token={token}"
    response = requests.get(url)
    result = []
    for lists in response.json():
        result.append({'id':lists.get('id'),'name':lists.get('name')})

    return result


filepath = './auth.txt'

parser = argparse.ArgumentParser()

if not os.path.exists(filepath):
    parser.add_argument("key", help="Your trello api key")
    parser.add_argument("token", help="Your trello api token")
else:
    key,token = get_auth(filepath)

print(key,token)

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true") # action="count", default=False

args = parser.parse_args()

boards_list=get_user_boards(key, token)
#boards_list[0]
pprint(get_user_lists(key,token,boards_list[0].get('id')))
