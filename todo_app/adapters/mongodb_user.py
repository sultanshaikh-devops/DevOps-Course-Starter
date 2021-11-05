import os, ssl, pymongo
from bson.objectid import ObjectId

class Connection():    
    def __init__(self): 
        self.mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
        self.mongo_collection_name = os.environ['MONGODB_COLLECTIONNAME']
        self.client = pymongo.MongoClient(self.mongo_connection_string, ssl_cert_reqs=ssl.CERT_NONE)
        self.mongo_db = self.client.todo_app
        self.collection = self.mongo_db.users
        
class mongodb_user(Connection):
    def get_totalusercount(self):
        return self.collection.find().count()
    
    def get_findusercount(self, qry):
        if qry != '':
            return self.collection.find(qry).count()

    def get_AllUsers(self):
        return self.collection.find()

    def get_qryItems(self, qry):
        if qry != '':
            return self.collection.find(qry)

    def create_user(self, username, role):
        post = {
            "username": username,
            "role": role
        }
        return self.collection.insert_one(post).inserted_id
   
    def delete_user(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})
    
    def update_user(self, id, username, role):
        post = {
            "username": username,
            "role": role
        }
        return self.collection.update_one({"_id": ObjectId(id)},{"$set": post})
    
    def get_user(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})
    
    def IsRoleAdmin(self, username):
        resp = False
        if username != '':
            results = self.collection.find({"username": username})
            for item in results:
                if item['role'] == 'admin':
                    resp = True
        return resp

    def IsRoleReader(self, username):
        resp = False
        if username != '':
            results = self.collection.find({"username": username})
            for item in results:
                if item['role'] == 'read':
                    resp = True
        return resp
    
    def IsRoleWriter(self, username):
        resp = False
        if username != '':
            results = self.collection.find({"username": username})
            for item in results:
                if item['role'] == 'write':
                    resp = True
        return resp
    
    def IsDisable(self, username):
        disable = True
        if username != '':
            results = self.collection.find({"username": username})
            for item in results:
                if (item['role'] == 'write') or (item['role'] == 'admin'):
                    disable = False
        return disable
    
