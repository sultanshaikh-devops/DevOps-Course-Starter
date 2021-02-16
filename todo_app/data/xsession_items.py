from flask import session

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]

lastid = {'id':2}

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
    all_items = session.get('items', _DEFAULT_ITEMS)
    sorted_items = sort(all_items)
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

    # Determine the ID: default value is pre set and increased as record is added therefore keep track of last id used.
   
    newid = lastid['id'] + 1 
    lastid['id'] = newid

    if status == '': 
        item = { 'id': newid, 'title': title, 'status': 'Not Started' }
    else:
        item = { 'id': newid, 'title': title, 'status': status}

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

    session['items'] = items
   
    return items

def find_index(dicts, key, value):
    for i, d in enumerate(dicts):
        if d.get(key) == value:
            return i
    else:
        raise ValueError('no dict with the key and value combination found')
