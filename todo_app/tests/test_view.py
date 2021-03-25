"""Unit tests for view.py"""

import pytest

from todo_app.view import *

def test_viewmodel_filterToDo_only():
    emptyViewModel = ViewModel([])
    assert len(emptyViewModel.todo) == 0

