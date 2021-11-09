import os, pytest, requests, time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
import pymongo
from todo_app.mongodbclient import *

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Loading environment variables 
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Create the new collection and save env to file   
    os.environ['MONGODB_COLLECTIONNAME'] = "tasks"
    
    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    mongo = MongoDBClient()
    mongo.collection.drop()


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

#test entries
def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App' 

def test_create_task(driver, app_with_temp_board):
    driver.get('http://localhost:5000/new')
    title_element = driver.find_element_by_id('title')
    title_element.send_keys("E2E Testing Task 1")

    description_element = driver.find_element_by_id('descarea')
    description_element.send_keys("Description E2E Test")
    description_element.submit()
    driver.implicitly_wait(10)
    task = driver.find_element_by_class_name('to-do-task')
    assert task != None
    assert "E2E Testing Task 1" in driver.page_source

@pytest.mark.depends(on=['test_create_task'])
def test_complete_task(driver, app_with_temp_board):
    updatestatus = driver.find_element_by_xpath("//a[contains(text(), 'Edit')]")
    updatestatus.click()
    status_element = driver.find_element_by_id('status')
    status_element.send_keys(Keys.DOWN)
    status_element.submit()
    driver.implicitly_wait(10)
    assert "Doing" in driver.page_source

@pytest.mark.depends(on=['test_complete_task'])
def test_delete_task(driver, app_with_temp_board):
    delete = driver.find_element_by_xpath("//a[contains(text(), 'Delete')]")
    delete.click()
    driver.implicitly_wait(10)   
    assert "E2E Testing Task 2" not in driver.page_source

