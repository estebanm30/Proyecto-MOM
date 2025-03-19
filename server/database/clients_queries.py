from .connection import get_db

db = get_db()
clients_collection = db["Clients"]

def find_all_clients():
    return clients_collection.find({})

def find_client(name):
    return clients_collection.find_one({"name": name})

def update_client(name, topic):
    return clients_collection.update_one({"name": name}, {"$set": topic})

def delete_client(name):
    return clients_collection.delete_one({"name": name})