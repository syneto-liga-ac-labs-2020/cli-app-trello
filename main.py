import click
import os
import requests
from pprint import pprint


class TrelloApi:
    def __init__(self, key, token):
        self.key = key
        self.token = token

    def __get(self, url):
        response = requests.get(url)
        result = []
        for item in response.json():
            result.append({'id': item.get('id'), 'name': item.get('name')})

        return result

    def get_user_boards(self):
        url = f'https://api.trello.com/1/members/me/boards?key={self.key}&token={self.token}'
        return self.__get(url)

    def get_user_lists(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/lists?key={self.key}&token={self.token}"
        return self.__get(url)



def get_auth(filepath):
    with open(filepath, 'r') as f:
        contents = f.readlines()
        return contents[0].strip('\n'), contents[1].strip('\n')
    return ("", "")




def get_user_cards(key, token, list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/cards?key={key}&token={token}"
    response = requests.get(url)
    result = []
    for card in response.json():
        result.append({'id': card.get('id'), 'nume': card.get('nume'), 'desc': card.get('desc')})
    return result


filepath = './auth.txt'


@click.group(help='Trello Api')
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable debug output",
)
@click.pass_context
def girafa(ctx, verbose):
    key, token = get_auth(filepath)
    ctx.obj = TrelloApi(key, token)


@girafa.command()
@click.pass_obj
def get_user_boards(api):
    user_boards = api.get_user_boards()
    print(user_boards)

@girafa.command()
@click.option('--board-id', help='Id of the board.')
@click.pass_obj
def get_user_lists(api, board_id):
    user_lists = api.get_user_lists(board_id)
    print(user_lists)

if __name__ == '__main__':
    girafa()



# parser = argparse.ArgumentParser()
#
# if not os.path.exists(filepath):
#     parser.add_argument("key", help="Your trello api key")
#     parser.add_argument("token", help="Your trello api token")
# else:
#     key,token = get_auth(filepath)
#
# print(key,token)
#
# parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true") # action="count", default=False
#
# args = parser.parse_args()
#
# boards_list=get_user_boards(key, token)
# #boards_list[0]
# list_ = get_user_lists(key,token,boards_list[0].get('id'))
#
# pprint(get_user_cards(key,token, list_[0].get('id')))
