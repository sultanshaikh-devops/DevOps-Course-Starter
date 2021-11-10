import datetime

class Card:
    def __init__(self, item):
        self.id = str(item['_id'])
        self.name = item['name']
        self.desc = item['desc']
        if (isinstance(item['due'], datetime.datetime)): 
            self.due = item['due'] 
        else: 
            self.due = datetime.datetime.strptime(str(item['due']).split('T')[0], '%Y-%m-%d')                      
        self.status = item['status']   
        self.dateLastActivity = item['dateLastActivity']   
