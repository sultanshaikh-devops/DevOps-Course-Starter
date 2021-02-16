import requests
import os 

class TrelloClient(object):

    def list_card(listid):
        url = os.environ['TRELLO_BASE_URL'] + 'lists/' + listid + '/cards'

        query = {
            'key': os.environ['TRELLO_API_KEY'],
            'token': os.environ['TRELLO_API_SECRET']
        }

        response = requests.request(
            "GET",
            url,
            params=query
        )

        return response        
    
    def create_card(cardname, listid, desc, due):
        url = os.environ['TRELLO_BASE_URL'] + 'cards'
        query = {
            'key': os.environ['TRELLO_API_KEY'],
            'token': os.environ['TRELLO_API_SECRET'],
            'idList': {listid},
            'name': {cardname},
            'desc': {desc},
            'due': {due}
        }

        response = requests.request(
            "POST",
            url,
            params=query
        )

        return response

    def delete_card(cardid):
        url = os.environ['TRELLO_BASE_URL'] + 'cards/' + cardid

        query = {
            'key': os.environ['TRELLO_API_KEY'],
            'token': os.environ['TRELLO_API_SECRET']
        }

        response = requests.request(
            "DELETE",
            url,
            params=query
        )

        return response

    def update_card(cardid, cardname, carddesc, listid, duedate):
        url = os.environ['TRELLO_BASE_URL'] + 'cards/' + cardid

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': os.environ['TRELLO_API_KEY'],
            'token': os.environ['TRELLO_API_SECRET'],
            'name': {cardname},
            'desc': {carddesc},
            'idList': {listid},
            'due': {duedate}
        }

        response = requests.request(
            "PUT",
            url,
            headers=headers,
            params=query
        )

        return response

    def get_card(cardid):
        url = os.environ['TRELLO_BASE_URL'] + 'cards/' + cardid

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': os.environ['TRELLO_API_KEY'],
            'token': os.environ['TRELLO_API_SECRET']
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response

    def get_boards():

        url = os.environ['TRELLO_BASE_URL'] + 'members/me/boards/all'

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': os.environ['TRELLO_API_KEY'],
            'token': os.environ['TRELLO_API_SECRET']
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response

    def get_lists(boardid):

        url = os.environ['TRELLO_BASE_URL'] + 'boards/' + boardid + '/lists'

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': os.environ['TRELLO_API_KEY'],
            'token': os.environ['TRELLO_API_SECRET']
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response