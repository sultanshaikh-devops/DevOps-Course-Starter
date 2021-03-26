import datetime

class ViewModel:
    def __init__(self, items):
        self._items = items
        
    @property
    def items(self):
        return self._items
    
    @property
    def todo(self):
        _todo_ls = [item for item in self._items if item.status == "Not Started"]
        return _todo_ls

    @property
    def doing(self):
        _doing_ls = [item for item in self._items if item.status == "In Progress"]
        return _doing_ls

    @property
    def recent_done_items(self):
        #_done_ls = [item for item in self._items if item.status == "Completed"]
        _done_ls = [item for item in self._items if item.dateLastActivity == str(datetime.datetime.today()).split()[0] and item.status == "Completed"]
        return _done_ls
    
    @property
    def show_all_done_items(self):
        _done_ls = [item for item in self._items if item.status == "Completed"]
        if len(_done_ls) < 5:
            return _done_ls
        else:
            _done_ls = [item for item in self._items if item.dateLastActivity == str(datetime.datetime.today()).split()[0] and item.status == "Completed"]
            return _done_ls

    @property
    def older_done_items(self):
       # _done_ls = [item for item in self._items if item.status == "Completed"]
        _done_ls = [item for item in self._items if item.dateLastActivity != str(datetime.datetime.today()).split()[0] and item.status == "Completed"]
        return _done_ls