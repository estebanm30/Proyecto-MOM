from connection import get_db

db = get_db()
clients_collection = db["Clients"]

seed_clients = [
    {"user": "client1", "password": "1234"},
    {"user": "client2", "password": "1234"},
    {"user": "client3", "password": "1234"},
    {"user": "client4", "password": "1234"},
    {"user": "client5", "password": "1234"},
    {"user": "client6", "password": "1234"},
]

for client in seed_clients:
    if not clients_collection.find_one({"user": client["user"]}):
        clients_collection.insert_one(client)
        print(f"User {client['user']} created.")
    else:
        print(f"User {client['user']} not longer available in database")

print("Seeding completed.")