"""Unit tests for view.py"""

#import pytest
from todo_app.view import ViewModel
from todo_app.models.card import Card
import datetime

sample_data = [
    {"idList": "123", "id":"1", "name":"Task1", "due":"2021-05-30", "dateLastActivity":"2021-05-16", "desc":"", "status":"Not Started"},
    {"idList": "123", "id":"2", "name":"Task2", "due":"2021-05-30", "dateLastActivity":"2021-01-16", "desc":"", "status":"In Progress"},
    {"idList": "123", "id":"3", "name":"Task3", "due":"2021-05-30", "dateLastActivity":"2021-02-16", "desc":"", "status":"Completed"},
    {"idList": "123", "id":"4", "name":"Task4", "due":"2021-05-30", "dateLastActivity":"2021-03-16", "desc":"", "status":"Not Started"},
    {"idList": "123", "id":"5", "name":"Task5", "due":"2021-05-30", "dateLastActivity":"2021-04-16", "desc":"", "status":"In Progress"},
    {"idList": "123", "id":"6", "name":"Task6", "due":"2021-01-30", "dateLastActivity":"2021-05-16", "desc":"", "status":"Completed"},
    {"idList": "123", "id":"8", "name":"Task7", "due":"2021-05-21", "dateLastActivity":str(datetime.datetime.today()).split()[0], "desc":"", "status":"Completed"}
]

cardslist = []
for card in sample_data:
    status = card['status']
    cardslist.append( Card(card=card, statuslabel=status) )    
 
def test_viewmodel_empty_filterToDo_only():
    emptyViewModel = ViewModel([])
    assert len(emptyViewModel.todo) == 0

def test_viewmodel_filterTodo_only():
    view_model = ViewModel(cardslist)
    result = view_model.todo 
    assert len(result) == 2
    assert result[0].status == "Not Started"

def test_viewmodel_empty_filterDoing_only():
    emptyViewModel = ViewModel([])
    assert len(emptyViewModel.doing) == 0

def test_viewmodel_filterDoing_only():
    view_model = ViewModel(cardslist)
    result = view_model.doing
    assert result[0].status == "In Progress"
    assert len(result) == 2

def test_viewmodel_empty_filterDone_only():
    emptyViewModel = ViewModel([])
    assert len(emptyViewModel.show_all_done_items) == 0

def test_viewmodel_filter_Show_all_done_items():
    view_model = ViewModel(cardslist)
    result = view_model.show_all_done_items
    assert result[0].status == "Completed"
    assert len(result) == 3

def test_viewmodel_filter_recent_done_items():
    view_model = ViewModel(cardslist)
    result = view_model.recent_done_items
    assert result[0].status == "Completed"
    assert len(result) == 1

def test_viewmodel_filter_older_done_items():
    view_model = ViewModel(cardslist)
    result = view_model.older_done_items
    assert result[0].status == "Completed"
    assert len(result) == 2