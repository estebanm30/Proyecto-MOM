import requests
import threading
import time

BASE_URL = "http://localhost:8000"
stop_event = threading.Event()


def listen_for_messages(token):
    while not stop_event.is_set():
        response = requests.get(
            f"{BASE_URL}/topic/messages/", params={"token": token})
        if response.status_code == 200:
            messages = response.json().get("messages", [])
            for msg in messages:
                print(
                    f"\n📩 New message on topic {msg['topic']}: {msg['message']}\n")
        time.sleep(2)


print("--------- CONNECT TO A SERVER ---------")

while True:
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    response = requests.post(f"{BASE_URL}/connect/",
                             json={"user": user, "password": password})

    if response.status_code == 200:
        connection = response.json()
        print("Connected to server")
        print("Token:", connection["token"])
        token = connection["token"]
        stop_event.clear()
        listener_thread = threading.Thread(
            target=listen_for_messages, args=(token,), daemon=True)
        listener_thread.start()

        while True:
            print("-------------------------")
            print("1. Create queue")
            print("2. Send message")
            print("3. Receive message")
            print("4. Delete queue")
            print("5. Create topic")
            print("6. Suscribe to topic")
            print("7. Publish message")
            print("8. Unsubscribe from topic")
            print("9. Exit")
            print("-------------------------")
            option = input("Select 1 option: ")
            if option == "1":
                name = input("Enter the queue name to create: ")
                response = requests.post(
                    f"{BASE_URL}/queue/create/", json={"name": name}, params={"token": token})
                print(response.json())
            elif option == "2":
                queue = input("Enter the queue name: ")
                message = input("Enter the message: ")
                response = requests.post(f"{BASE_URL}/queue/send/",
                                         params={"queueName": queue, "message": message, "token": token})
                print(response.json())
            elif option == "3":
                queue = input("Ingrese el nombre de la cola: ")
                response = requests.get(f"{BASE_URL}/queue/receive/",
                                        params={"queueName": queue, "token": token})
                print(response.json())
            elif option == "4":
                queue = input("Ingrese el nombre de la cola: ")
                response = requests.delete(f"{BASE_URL}/queue/",
                                           params={"queueName": queue, "token": token})
                print(response.json())
            elif option == "5":
                name = input("Enter the topic name to create: ")
                response = requests.post(
                    f"{BASE_URL}/topic/create/", json={"name": name}, params={"token": token})
                print(response.json())
            elif option == "6":
                topic = input("Enter the topic name: ")
                response = requests.put(f"{BASE_URL}/topic/subscribe/",
                                         params={"topic_name": topic, "token": token})
                print(response.json())
            elif option == "7":
                topic = input("Enter the topic name: ")
                message = input("Enter the message: ")
                response = requests.post(f"{BASE_URL}/topic/publish/",
                                         params={"topic_name": topic, "message": message, "token": token})
                print(response.json())
            elif option == "8":
                topic = input("Enter the topic name: ")
                response = requests.put(f"{BASE_URL}/topic/unsubscribe/",
                                        params={"topic_name": topic, "token": token})
                print(response.json())
            elif option == "9":
                stop_event.set()
                listener_thread.join()
                break
    else:
        print("Connection failed")
