import os, pytest, requests, time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app

#from requests.models import Response
# Loading environment variables 
file_path = find_dotenv('.env')
load_dotenv(file_path, override=True)

BASE_URL = "https://api.trello.com/1/"
API_KEY = os.environ.get('TRELLO_API_KEY')
TOKEN = os.environ.get('TRELLO_API_SECRET')

def create_trello_board():
    params = {
        'key': API_KEY,
        'token': TOKEN,
        'name': "E2E Testing",
    }
    response = requests.post(BASE_URL + 'boards', params=params)
    return response

def delete_trello_board(board_id):
    params = {
        'key': API_KEY,
        'token': TOKEN,
    }
    response = requests.delete(BASE_URL + f'boards/{board_id}', params=params)
    return response

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    create_board_response = create_trello_board()
    if create_board_response.status_code == 200:
        board_id = create_board_response.json()['id']
        board_name = 'E2E Testing'
        os.environ['TRELLO_BOARD_NAME'] = board_name 
    else:
        print('create board failure' + create_board_response.status_code)
    
    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    del_board_response = delete_trello_board(board_id)
    if del_board_response.status_code == 200:
        print(f'Board deleted passed {del_board_response.status_code}')
    else:
        print(f'Board delete failed {del_board_response.status_code}')

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

#test entries
def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App' 

def test_create_task(driver, app_with_temp_board):
    #time.sleep(3)​
    driver.get('http://localhost:5000/new')
    title_element = driver.find_element_by_id('title')
    title_element.send_keys("E2E Testing Task 1")

    description_element = driver.find_element_by_id('descarea')
    description_element.send_keys("Description E2E Test")
    description_element.submit()
    driver.implicitly_wait(3)
    task = driver.find_element_by_class_name('to-do-task')
    assert task != None
    assert "E2E Testing Task 1" in driver.page_source

def test_complete_task(driver, app_with_temp_board):
    updatestatus = driver.find_element_by_xpath("//a[contains(text(), 'Edit')]")
    updatestatus.click()
    status_element = driver.find_element_by_id('status')
    status_element.send_keys('In Progress')
    status_element.submit()
    driver.implicitly_wait(3)
    assert "In Progress" in driver.page_source

def test_delete_task(driver, app_with_temp_board):
    driver.find_element_by_xpath("//a[contains(text(), 'Delete')]").click()   
    assert "E2E Testing Task 1" not in driver.page_source


