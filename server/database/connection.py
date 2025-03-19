import pymongo
from dotenv import load_dotenv
import os
load_dotenv()
DB_ADDRESS = os.getenv("DB_ADDRESS")


def get_db():
    client = pymongo.MongoClient(DB_ADDRESS)
    db = client["MomDB"]

    if "Queues" not in db.list_collection_names():
        db.create_collection("Queues")
    if "Topics" not in db.list_collection_names():
        db.create_collection("Topics")
    if "Clients" not in db.list_collection_names():
        db.create_collection("Clients")

    return db
