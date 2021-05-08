class Card:
    def __init__(self, card, statuslabel):
        self.listid = card['idList']
        self.id = card['id']                     
        self.status = statuslabel
        self.title = card['name']
        self.due = card['due']
        self.desc = card['desc']   
        self.dateLastActivity = card['dateLastActivity']   