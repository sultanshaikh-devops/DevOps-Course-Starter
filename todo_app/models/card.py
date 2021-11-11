import datetime

class Card:
    def __init__(self, item):
        self.id = str(item['_id'])
        self.name = item['name']
        self.desc = item['desc']
        if (isinstance(item['due'], datetime.datetime)): 
            self.due = (datetime.datetime.strptime((item['due']).strftime("%Y-%m-%d"), '%Y-%m-%d')).strftime("%Y-%m-%d")
        else: 
            self.due = datetime.datetime.strptime(str(item['due']).split('T')[0], '%Y-%m-%d')                      
        self.status = item['status']   
        self.dateLastActivity = item['dateLastActivity']   
