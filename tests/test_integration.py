import pytest
import mongomock
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from unittest.mock import Mock, patch
import datetime
from todo_app.mongodbclient import *


sample_data = [
    {"_id":"617c478ba79ad94f59ba815a", "name":"Task1", "due":"2021-10-26T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task1", "status":"To Do"},
    {"_id":"617c478ba79ad94f59ba815b", "name":"Task2", "due":"2021-10-27T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task2", "status":"Doing"},
    {"_id":"617c478ba79ad94f59ba815c", "name":"Task3", "due":"2021-10-28T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task3", "status":"Done"},
    {"_id":"617c478ba79ad94f59ba815d", "name":"Task4", "due":"2021-10-29T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task4", "status":"To Do"},
    {"_id":"617c478ba79ad94f59ba815e", "name":"Task5", "due":"2021-10-26T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task5", "status":"Doing"},
    {"_id":"617c478ba79ad94f59ba815f", "name":"Task6", "due":"2021-10-30T00:00:00.000+00:00", "dateLastActivity":"2021-10-26T00:00:00.000+00:00", "desc":"Task6", "status":"Done"},
    {"_id":"617c478ba79ad94f59ba815g", "name":"Task7", "due":"2021-10-25T00:00:00.000+00:00", "dateLastActivity":datetime.datetime.strptime((datetime.datetime.utcnow()).strftime("%Y-%m-%d"), '%Y-%m-%d'), "desc":"Task7", "status":"Done"}
]

# @pytest.fixture(autouse=True)
# def patch_mongo(monkeypatch):
#     db = mongomock.MongoClient()
#     def fake_mongo():
#         return db
#     monkeypatch.setattr('mongo_stuff.mongo', fake_mongo)

# @pytest.fixture
# def test_update_one_with_upsert(self):
#         collection = mongomock.MongoClient().db.collection

#         filter_doc = {'_id': '1', 'field': 0}
#         update_doc = {'$inc': {'field': 123}}

#         self.hook.update_one(collection, filter_doc, update_doc, upsert=True)

#         result_obj = collection.find_one(filter='1')
        # self.assertEqual(123, result_obj['field']) 


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    os.environ['MONGO_CONNECTION_STRING'] = "mongodb://admin:xyz@server.example.com/todo_app?retryWrites=true&w=majority"
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

@mongomock.patch(servers=(('server.example.com', 27017),))
def test_index_page(client):
    mongo = MongoDBClient()
    response = mongo.create_task(
        name = "Task8",
        due = "2021-10-26",
        desc = "Task8"
    )
    response = client.get('/')
    assert response.status_code == 200
    assert 'Task8' in response.data.decode()


# def mock_requests_get(url, headers, params):
#     if url == f'https://api.trello.com/1/members/me/boards/all':
#         response = Mock()
#         response.status_code = 200
#         response.json.return_value = sample_trello_board_response
#         return response
#     boardid = sample_trello_board_response[0]['id']

    
#     if url == f'https://api.trello.com/1/boards/{boardid}/lists':
#         response = Mock()
#         response.status_code = 200
#         response.json.return_value = sample_trello_lists_response
#         return response

#     todoid = sample_trello_lists_response[0]['id']
#     if url == f'https://api.trello.com/1/lists/{todoid}/cards':
#         response = Mock()
#         response.status_code = 200
#         response.json.return_value = sample_trello_todo_response
#         return response

#     doingid = sample_trello_lists_response[1]['id']
#     if url == f'https://api.trello.com/1/lists/{doingid}/cards':
#         response = Mock()
#         response.status_code = 200
#         response.json.return_value = sample_trello_doing_response
#         return response

#     doneid = sample_trello_lists_response[2]['id']
#     if url == f'https://api.trello.com/1/lists/{doneid}/cards':
#         response = Mock()
#         response.status_code = 200
#         response.json.return_value = sample_trello_done_response
#         return response
#     return None