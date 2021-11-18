import os, datetime, ssl, pymongo
import pymongo
from bson.objectid import ObjectId

class Connection():    
    def __init__(self): 
        self.mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
        self.mongo_collection_name = os.environ['MONGODB_COLLECTION_NAME']
        self.client = pymongo.MongoClient(self.mongo_connection_string, ssl_cert_reqs=ssl.CERT_NONE)
        self.mongo_db = self.client.todo_app
        self.collection = self.mongo_db[self.mongo_collection_name]
        
class mongodb_todo(Connection):
    def get_AllItems(self):
        return self.collection.find()

    def get_qryItems(self, qry):
        if qry != '':
            return self.collection.find(qry)

    def create_task(self, name, desc, due):
        if due == "":
            due = (datetime.date.today()).strftime("%Y-%m-%d")

        post = {
            "name": name,
            "desc": desc,
            "status": "To Do",
            "due": datetime.datetime.strptime(due, '%Y-%m-%d'),
            "dateLastActivity": datetime.datetime.strptime((datetime.datetime.utcnow()).strftime("%Y-%m-%d"), '%Y-%m-%d')
        }
        return self.collection.insert_one(post).inserted_id
   
    def delete_task(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})
    
    def update_task(self, id, name, desc, due, status):
        post = {
            "name": name,
            "desc": desc,
            "status": status,
            "due": datetime.datetime.strptime(due, '%Y-%m-%d'),
            "dateLastActivity": datetime.datetime.strptime((datetime.datetime.utcnow()).strftime("%Y-%m-%d"), '%Y-%m-%d')
        }
        return self.collection.update_one({"_id": ObjectId(id)},{"$set": post})
    
    def get_task(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})
    
    def get_today_done_task(self):
        qry = {
            "status": "Done",
            "dateLastActivity": datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d')    
        }

        return self.get_qryItems(qry)
    
    def get_older_done_task(self):
        qry = {
            "status": "Done",
            "dateLastActivity": {"$lt": datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d')}    
        }
        return self.get_qryItems(qry)
    
    
