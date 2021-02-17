import requests
import os

class Card:
    def __init__(self, json, statusName):        
        self.listid = json['idList']
        self.id = json['id']                     
        self.status = statusName
        self.title = json['name']
        self.due = json['due']
        self.desc = json['desc']

class TrelloClient:    
    def __init__(self):
        self.url = os.environ['TRELLO_BASE_URL'] 
        self.key = os.environ['TRELLO_API_KEY']
        self.token = os.environ['TRELLO_API_SECRET']
        self.header = "application/json"

        self.headers = {
            "Accept": self.header
        }

        self.query = {
            'key' : self.key,
            'token': self.token
        }

class TrelloBoard(TrelloClient):
    def get_BoardList(self):
        response = requests.request(
            "GET",
            self.url + 'members/me/boards/all',
            headers=self.headers,
            params=self.query
        )
        return response

class TrelloList(TrelloClient):
    def get_List(self, id):
        response = requests.request(
            "GET",
            self.url + 'boards/' + id + '/lists',
            headers=self.headers,
            params=self.query
        )
        return response

class TrelloCard(TrelloClient):
    def get_List(self, id):
        response = requests.request(
            "GET",
            self.url + 'lists/' + id + '/cards',
            headers=self.headers,
            params=self.query
        )
        return response
    
    def get_Card(self, id):
        response = requests.request(
            "GET",
            self.url + 'cards/' + id,
            headers=self.headers,
            params=self.query
        )
        return response       

    def create_Card(self, id, name, desc, due):
        query = self.query
        query['idList'] = id
        query['name'] = name
        query['desc'] = desc
        query['due'] = due

        response = requests.request(
            "POST",
            self.url + 'cards',
            headers=self.headers,
            params=query
        )
        return response   

    def update_Card(self, id, listId, name, desc, due):
        query = self.query
        query['idList'] = listId
        query['name'] = name
        query['desc'] = desc
        query['due'] = due

        response = requests.request(
            "PUT",
            self.url + 'cards/' + id,
            headers=self.headers,
            params=query
        )
        return response 

    def delete_Card(self, id):
        response = requests.request(
            "DELETE",
            self.url + 'cards/' + id,
            headers=self.headers,
            params=self.query
        )
        return response 
        