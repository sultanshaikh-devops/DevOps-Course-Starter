class ViewModel:
    def __init__(self, items):
        self._items = items
        
    @property
    def items(self):
        return self._items
    
    @property
    def todo(self):
        todo_dict = [item for item in self._items if item.status == "Not Started"]
        return todo_dict

