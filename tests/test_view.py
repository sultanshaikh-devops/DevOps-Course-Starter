"""Unit tests for view.py"""

#import pytest
from todo_app.view import ViewModel

def test_viewmodel_empty_filterToDo_only():
    emptyViewModel = ViewModel([])
    assert len(emptyViewModel.todo) == 0

def test_viewmodel_filterTodo_only():
    view_model = ViewModel([{"title":"Task1", "due date":"2021-03-25", "status":"Not Started"}])
    assert view_model.items[0]['status'] == "Not Started"

def test_viewmodel_empty_filterDoing_only():
    emptyViewModel = ViewModel([])
    assert len(emptyViewModel.doing) == 0

def test_viewmodel_filterDoing_only():
    view_model = ViewModel([{"title":"Task1", "due date":"2021-03-25", "status":"In Progress"}])
    assert view_model.items[0]['status'] == "In Progress"

def test_viewmodel_empty_filterDone_only():
    emptyViewModel = ViewModel([])
    assert len(emptyViewModel.show_all_done_items) == 0

def test_viewmodel_filterDone_only():
    view_model = ViewModel([{"title":"Task1", "due date":"2021-03-25", "status":"Completed"}])
    assert view_model.items[0]['status'] == "Completed"