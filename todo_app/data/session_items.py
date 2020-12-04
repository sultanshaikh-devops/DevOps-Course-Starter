from flask import session

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]

def sort(dicts):
    #using sorted and lambda to return list sorted
    #by status (Not Started/Completed)
    return sorted(dicts, key = lambda i: i['status'],reverse=True)




def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    All_items = session.get('items', _DEFAULT_ITEMS)
    sorted_items = sort(All_items)
    #return session.get('items', _DEFAULT_ITEMS)
    return sorted_items


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title, status):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    #id = items[-1]['id'] + 1 if items else 0
    id = 0
    checkid = []
    for item in items:
        checkid.append(item['id'])
    
    if items != []:
        matchfound = True
        while matchfound:
            if (id in checkid):
                #print(str(id) + " found!")
                id = id + 1
            else:
                matchfound = False
                #print(str(id)) 

    if status == '': 
        item = { 'id': id, 'title': title, 'status': 'Not Started' }
    else:
        item = { 'id': id, 'title': title, 'status': status}

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

def delete_item(id):
    """
    Delete an existing item in the session. If no existing item matches the ID of the specified item, nothing is deleted.

    Args:
        item: The item to delete.
    """
    items = get_items()
    indexNumber = find_index(items, 'id', id)
    del items[indexNumber]
    #updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = items
   
    return items

def find_index(dicts, key, value):
    class Null: pass
    for i, d in enumerate(dicts):
        if d.get(key, Null) == value:
            return i
    else:
        raise ValueError('no dict with the key and value combination found')
