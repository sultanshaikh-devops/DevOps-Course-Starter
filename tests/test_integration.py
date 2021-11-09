import pytest
import mongomock
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from unittest.mock import Mock, patch
import datetime
from todo_app.mongodbclient import *

storeConString  = ""

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    #os.environ['MONGO_CONNECTION_STRING'] = "mongodb://admin:xyz@server.example.com/todo_app?retryWrites=true&w=majority"
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


