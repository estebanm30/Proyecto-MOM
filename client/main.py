from termcolor import colored
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
            for message in messages:
                print(colored(
                    f"\n📩 New message on topic {message['topic']}: {message['message']}\n", "green"))
        time.sleep(2)


print("--------- CONNECT TO A SERVER ---------")

while True:

    print(colored("Type 'exit' to quit", "red"))
    user = input("Enter your username: ")
    if user == "exit":
        break
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
        print("\033c", end="")
        while True:
            print("-------------------------")
            print("1. Queues")
            print("2. Topics")
            print("3. Exit")
            print("-------------------------")
            option = input("Select 1 option: ")
            print("\033c", end="")
            if option == "1":
                while True:
                    response = requests.get(
                        f"{BASE_URL}/queue/", params={"token": token})
                    if response.status_code == 200:
                        queues = response.json()
                        print("\nQueues:")
                        for queue in queues:
                            print(colored(queue, "yellow"))

                    print("-------------------------")
                    print("1. Create queue")
                    print("2. Send message")
                    print("3. Receive message")
                    print("4. Delete queue")
                    print("5. Go back")
                    print("-------------------------")
                    option = input("Select 1 option: ")

                    if option == "1":
                        queue_name = input("Enter the queue name to create: ")
                        response = requests.post(
                            f"{BASE_URL}/queue/create/", json={"name": queue_name}, params={"token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "2":
                        queue_name = input("Enter the queue name: ")
                        message = input("Enter the message: ")
                        response = requests.post(f"{BASE_URL}/queue/send/",
                                                 params={"queue_name": queue_name, "message": message, "token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "3":
                        queue_name = input("Ingrese el nombre de la cola: ")
                        response = requests.get(f"{BASE_URL}/queue/receive/",
                                                params={"queue_name": queue_name, "token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "green"))

                    elif option == "4":
                        queue_name = input("Ingrese el nombre de la cola: ")
                        response = requests.delete(f"{BASE_URL}/queue/",
                                                   params={"queue_name": queue_name, "token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "5":
                        print("\033c", end="")
                        break

            elif option == "2":
                while True:
                    response = requests.get(
                        f"{BASE_URL}/topic/", params={"token": token})
                    if response.status_code == 200:
                        topics = response.json()
                        print("\nTopics:")
                        for topic in topics:
                            print(colored(topic, "yellow"))

                    print("-------------------------")
                    print("1. Create topic")
                    print("2. Suscribe to topic")
                    print("3. Publish message")
                    print("4. Unsubscribe from topic")
                    print("5. Delete topic")
                    print("6. Go back ")
                    print("-------------------------")
                    option = input("Select 1 option: ")

                    if option == "1":
                        topic_name = input("Enter the topic name to create: ")
                        response = requests.post(
                            f"{BASE_URL}/topic/create/", json={"name": topic_name}, params={"token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "2":
                        topic_name = input("Enter the topic name: ")
                        response = requests.put(f"{BASE_URL}/topic/subscribe/",
                                                params={"topic_name": topic_name, "token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "3":
                        topic_name = input("Enter the topic name: ")
                        message = input("Enter the message: ")
                        response = requests.post(f"{BASE_URL}/topic/publish/",
                                                 params={"topic_name": topic_name, "message": message, "token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "4":
                        topic_name = input("Enter the topic name: ")
                        response = requests.put(f"{BASE_URL}/topic/unsubscribe/",
                                                params={"topic_name": topic_name, "token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "5":
                        topic_name = input("Enter the topic name: ")
                        response = requests.delete(f"{BASE_URL}/topic/",
                                                   params={"topic_name": topic_name, "token": token})
                        print("\033c", end="")
                        print(colored(response.json(), "yellow"))

                    elif option == "6":
                        print("\033c", end="")
                        break
            elif option == "3":
                stop_event.set()
                listener_thread.join()
                break
            else:
                print("\033c", end="")
                print(colored("Invalid option", "red"))
    else:
        print("Connection failed")
