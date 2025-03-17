from .connection import get_db

db = get_db()
collection = db["Queues"]
topics_collection = db["Topics"]

def insert_queue(queue):
    return collection.insert_one(queue)


def find_all_queues():
    return collection.find({})


def find_queue(name):
    return collection.find_one({"name": name})


def update_queue(name, messages):
    return collection.update_one({"name": name}, {"$set": {"messages": messages}})


def delete_queue(name):
    return collection.delete_one({"name": name})

def insert_topic(topic):
    return topics_collection.insert_one(topic)

def find_all_topics():
    return topics_collection.find({})

def find_topic(name):
    return topics_collection.find_one({"name": name})

def update_topic(name, messages):
    return topics_collection.update_one({"name": name}, {"$set": {"messages": messages}})

def delete_topic(name):
    return topics_collection.delete_one({"name": name})