import pytest
import mongomock
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from unittest.mock import Mock, patch
import datetime
from todo_app.adapters.mongodb_todo import *

storeConString  = ""

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('server.example.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    mongo = mongodb_todo()
    response = mongo.create_task(
        name = "Task8",
        due = "2021-10-26",
        desc = "Task8"
    )
    response = client.get('/home')
    assert response.status_code == 200
    assert 'Task8' in response.data.decode()


