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

    def __post(self, url, data):
        response = requests.post(url, data)
        if response.status_code == 200:
            return True
        return False

    def __put(self, url, data):
        response = requests.put(url, data)
        if response.status_code == 200:
            return True
        return False

    def __delete(self, url):
        response = requests.delete(url)
        if response.status_code == 200:
            return True
        return False

    def get_user_boards(self):
        url = f"https://api.trello.com/1/members/me/boards?key={self.key}&token={self.token}"
        return self.__get(url)

    def get_user_lists(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/lists?key={self.key}&token={self.token}"
        return self.__get(url)

    def add_user_cards(self, list_id, name):
        url = f'https://api.trello.com/1/cards?key={self.key}&token={self.token}'
        is_card_added = self.__post(url, {'idList': list_id, 'name': name})
        if is_card_added:
            pprint('card added succesfully')
        else:
            pprint('card failed to add')

    def edit_user_card(self, card_id, name, description):
        url = f'https://api.trello.com/1/cards/{card_id}?key={self.key}&token={self.token}'
        is_card_updated = self.__put(url, {'id': card_id, 'name': name, 'desc' : description})
        if is_card_updated:
            pprint('card updated succesfully')
        else:
            pprint('card failed to update')

    def get_user_card(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards?key={self.key}&token={self.token}"
        response = requests.get(url)
        result = []
        for card in response.json():
            result.append({'id': card.get('id'), 'name': card.get('name'), 'desc': card.get('desc')})
        return result

    def delete_user_card(self, card_id):
    	url = f'https://api.trello.com/1/cards/{card_id}?key={self.key}&token={self.token}'
    	is_card_deleted = self.__delete(url)
    	if is_card_deleted:
    		pprint('Card deleted succesfully')
    	else:
    		pprint('Could not delete card')

def get_auth(filepath):
    with open(filepath, 'r') as f:
        contents = f.readlines()
        return contents[0].strip('\n'), contents[1].strip('\n')
    return ("", "")


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

@girafa.group(help='Cards')
@click.pass_context
def cards(ctx):
    pass

@cards.command(help ='Delete')
@click.option('--card-id', help='id of the card')
@click.pass_obj
def delete(api, card_id):
	api.delete_user_card(card_id)

@girafa.group(help='Lists')
@click.pass_context
def lists(ctx):
    pass

@lists.command(help='Add a list')
@click.pass_obj
def add(api):
    pprint("Added list")

@cards.command(help='Add a card')
@click.pass_obj
def add(api):
    pprint("Added card")

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


@girafa.command()
@click.option('--list-id', help='Id of the list the card should be created in.')
@click.option('--name', help='The name of the card')
@click.pass_obj
def add_user_card(api, list_id, name):
    api.add_user_cards(list_id, name)


@girafa.command()
@click.option('--list-id', help='Id of the list the card we want to see.')
@click.pass_obj
def get_user_cards(api, list_id):
    pprint(api.get_user_card(list_id))

@girafa.command()
@click.option('--card-id', help='id of the card')
@click.option('--name', help='name of the card')
@click.option('--description', help='description of the card')
@click.pass_obj
def update_user_card(api, card_id,name,description):
   api.edit_user_card(card_id,name,description)


if __name__ == '__main__':
    girafa()
