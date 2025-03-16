import requests

BASE_URL = "http://localhost:8000"
print("--------- CONNECT TO A SERVER ---------")

while True:
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    response = requests.post(f"{BASE_URL}/connect/", json={"user": user, "password":password})

    if response.status_code == 200:
        connection = response.json()
        print("Connected to server")
        print("Token:", connection["token"])
        token = connection["token"]

    while True:
        print("-------------------------")
        print("1. Create queue")
        print("2. Send message")
        print("3. Receive message")
        print("4. Delete queue")
        print("5. Exit")
        print("-------------------------")
        option = input("Select 1 option: ")
        if option == "1":
            name = input("Enter the queue name to create: ")
            response = requests.post(
                f"{BASE_URL}/queue/create/", json={"name": name} params={"token": token})
            print(response.json())
        elif option == "2":
            queue = input("Enter the queue name: ")
            message = input("Enter the message: ")
            response = requests.post(f"{BASE_URL}/queue/send/",
                                    params={"queueName": queue, "message": message , "token": token})
            print(response.json())
        elif option == "3":
            queue = input("Ingrese el nombre de la cola: ")
            response = requests.get(f"{BASE_URL}/queue/receive/",
                                    params={"queueName": queue, "token": token})
            print(response.json())
        elif option == "4":
            queue = input("Ingrese el nombre de la cola: ")
            response = requests.delete(f"{BASE_URL}/queue/",
                                    params={"queueName": queue})
            print(response.json())
        elif option == "5":
            break
    else:
        print("Connection failed")
