from .connection import get_db

db = get_db()
collection = db["Queues"]
topics_collection = db["Topics"]

def insert_queue(queue):
    return collection.insert_one(queue)


def find_all_queues():
    return list(collection.find({}))


def find_queue(name):
    return collection.find_one({"name": name})


def update_queue(name, queue):
    return collection.update_one({"name": name}, {"$set": queue})


def delete_queue(name):
    return collection.delete_one({"name": name})

