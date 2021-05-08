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
    }]

sample_trello_todotasks_response = [
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
    }
]
sample_trello_doingtasks_response = []
sample_trello_donetasks_response = []

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
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


def mock_get_lists(url, headers, params):
    if url == f'https://api.trello.com/1/members/me/boards/all':
        response = Mock()
        response.status_code = 200
        response.json.return_value = sample_trello_board_response
        return response
    boardid = sample_trello_board_response[0]['id']
    
    if url == f'https://api.trello.com/1/boards/{boardid}/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.status_code = 200
        response.json.return_value = sample_trello_lists_response
        return response

    todoid = sample_trello_lists_response[0]['id']
    if url == f'https://api.trello.com/1/lists/{todoid}/cards':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.status_code = 200
        response.json.return_value = sample_trello_todotasks_response
        return response

    doingid = sample_trello_lists_response[1]['id']
    if url == f'https://api.trello.com/1/lists/{doingid}/cards':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.status_code = 200
        response.json.return_value = sample_trello_doingtasks_response
        return response

    doneid = sample_trello_lists_response[2]['id']
    if url == f'https://api.trello.com/1/lists/{doneid}/cards':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.status_code = 200
        response.json.return_value = sample_trello_donetasks_response
        return response
    return None