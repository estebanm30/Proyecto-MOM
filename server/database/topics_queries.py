from .connection import get_db

db = get_db()
topics_collection = db["Topics"]

def insert_topic(topic):
    return topics_collection.insert_one(topic)

def find_all_topics():
    return topics_collection.find({})

def find_topic(name):
    return topics_collection.find_one({"name": name})

def update_topic(name, topic):
    return topics_collection.update_one({"name": name}, {"$set": topic})

def delete_topic(name):
    return topics_collection.delete_one({"name": name})