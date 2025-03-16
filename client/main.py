import requests

BASE_URL = "http://localhost:8000"

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
            f"{BASE_URL}/queue/create/", json={"name": name})
        print(response.json())
    elif option == "2":
        queue = input("Enter the queue name: ")
        message = input("Enter the message: ")
        response = requests.post(f"{BASE_URL}/queue/send/",
                                 params={"queueName": queue, "message": message})
        print(response.json())
    elif option == "3":
        queue = input("Ingrese el nombre de la cola: ")
        response = requests.get(f"{BASE_URL}/queue/receive/",
                                params={"queueName": queue})
        print(response.json())
    elif option == "4":
        queue = input("Ingrese el nombre de la cola: ")
        response = requests.delete(f"{BASE_URL}/queue/",
                                   params={"queueName": queue})
        print(response.json())
    elif option == "5":
        break
