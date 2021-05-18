import pytest
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from unittest.mock import Mock, patch

sample_trello_board_response = [{"name":"ToDo","id":"1234567"}]
sample_trello_lists_response = [
    {
        "id": "602a48f933d6e282f2f1b055",
        "name": "To Do",
        "idBoard": "602a48f933d6e282f2f1b054"
    },
    {
        "id": "602a48f933d6e282f2f1b056",
        "name": "Doing",
        "idBoard": "602a48f933d6e282f2f1b054"
    },
    {
        "id": "602a48f933d6e282f2f1b057",
        "name": "Done",
        "idBoard": "602a48f933d6e282f2f1b054"
    }
]
sample_trello_todo_response = [
    {
        "id": "602d523cbe5a9c881827aea0",
        "dateLastActivity": "2021-03-07T21:29:20.664Z",
        "desc": "Job1\r\nHello",
        "idBoard": "602a48f933d6e282f2f1b054",
        "idList": "602a48f933d6e282f2f1b055",
        "idMembersVoted": [],
        "idShort": 20,
        "idLabels": [],
        "name": "To Do Task Test",
        "pos": 65536,
        "shortLink": "TacXfGbs",
        "due": "2021-02-05T00:00:00.000Z"
    },
    {
        "id": "602d523cbe5a9c881827aea1",
        "dateLastActivity": "2021-03-07T21:29:20.664Z",
        "desc": "Job2\r\nHello",
        "idBoard": "602a48f933d6e282f2f1b054",
        "idList": "602a48f933d6e282f2f1b055",
        "idMembersVoted": [],
        "idShort": 20,
        "idLabels": [],
        "name": "Second Task",
        "pos": 65536,
        "shortLink": "TacXfGbs",
        "due": "2021-02-05T00:00:00.000Z"
    }
]
sample_trello_doing_response = [
    {
        "id": "602d523cbe5a9c881827aea3",
        "dateLastActivity": "2021-03-07T21:29:20.664Z",
        "desc": "Job1\r\nHello",
        "idBoard": "602a48f933d6e282f2f1b054",
        "idList": "602a48f933d6e282f2f1b056",
        "idMembersVoted": [],
        "idShort": 20,
        "idLabels": [],
        "name": "First doing task",
        "pos": 65536,
        "shortLink": "TacXfGbs",
        "due": "2021-02-05T00:00:00.000Z"
    },
    {
        "id": "602d523cbe5a9c881827aea4",
        "dateLastActivity": "2021-03-07T21:29:20.664Z",
        "desc": "Job2\r\nHello",
        "idBoard": "602a48f933d6e282f2f1b054",
        "idList": "602a48f933d6e282f2f1b056",
        "idMembersVoted": [],
        "idShort": 20,
        "idLabels": [],
        "name": "Second doing task",
        "pos": 65536,
        "shortLink": "TacXfGbs",
        "due": "2021-02-05T00:00:00.000Z"
    }
]
sample_trello_done_response = [    
    {
        "id": "602d523cbe5a9c881827aea5",
        "dateLastActivity": "2021-03-07T21:29:20.664Z",
        "desc": "Job1\r\nHello",
        "idBoard": "602a48f933d6e282f2f1b054",
        "idList": "602a48f933d6e282f2f1b057",
        "idMembersVoted": [],
        "idShort": 20,
        "idLabels": [],
        "name": "First done task",
        "pos": 65536,
        "shortLink": "TacXfGbs",
        "due": "2021-02-05T00:00:00.000Z"
    },
    {
        "id": "602d523cbe5a9c881827aea6",
        "dateLastActivity": "2021-03-07T21:29:20.664Z",
        "desc": "Job2\r\nHello",
        "idBoard": "602a48f933d6e282f2f1b054",
        "idList": "602a48f933d6e282f2f1b057",
        "idMembersVoted": [],
        "idShort": 20,
        "idLabels": [],
        "name": "Second done task",
        "pos": 65536,
        "shortLink": "TacXfGbs",
        "due": "2021-02-05T00:00:00.000Z"
    }
]

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def mock_getrequest():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = mock_get_lists
        yield mock_get

def test_index_page(mock_getrequest, client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'To Do Task Test' in response.data.decode()
    assert 'failure test' not in response.data.decode()


def mock_get_lists(url, headers, params):
    if url == f'https://api.trello.com/1/members/me/boards/all':
        response = Mock()
        response.status_code = 200
        response.json.return_value = sample_trello_board_response
        return response
    boardid = sample_trello_board_response[0]['id']

    
    if url == f'https://api.trello.com/1/boards/{boardid}/lists':
        response = Mock()
        response.status_code = 200
        response.json.return_value = sample_trello_lists_response
        return response

    todoid = sample_trello_lists_response[0]['id']
    if url == f'https://api.trello.com/1/lists/{todoid}/cards':
        response = Mock()
        response.status_code = 200
        response.json.return_value = sample_trello_todo_response
        return response

    doingid = sample_trello_lists_response[1]['id']
    if url == f'https://api.trello.com/1/lists/{doingid}/cards':
        response = Mock()
        response.status_code = 200
        response.json.return_value = sample_trello_doing_response
        return response

    doneid = sample_trello_lists_response[2]['id']
    if url == f'https://api.trello.com/1/lists/{doneid}/cards':
        response = Mock()
        response.status_code = 200
        response.json.return_value = sample_trello_done_response
        return response
    return None