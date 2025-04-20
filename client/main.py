from termcolor import colored
import requests
import threading
import time
from zookeeper import get_queue_server, get_all_queues, get_all_topics, get_servers, get_random_server, remove_token

BASE_URL = "http://localhost:8000"
stop_event = threading.Event()


def check_servers(server_address):
    if not server_address:
        print(colored("❌ Queue not found in Zookeeper!", "red"))
        return True
    if not server_address in get_servers():
        print(colored("❌ Server Not Online!", "red"))
        return True
    return False


def listen_for_messages(token):
    while not stop_event.is_set():
        servers = get_servers()
        if not servers:
            print(colored("⚠ No servers available in Zookeeper!", "red"))
            time.sleep(2)
            continue

        for server in servers:
            try:
                response = requests.get(
                    f"http://{server}/topic/messages/", params={"token": token}, timeout=5
                )

                if response.status_code == 200:
                    messages = response.json().get("messages", [])
                    for message in messages:
                        print(
                            colored(f"📨 Received messages from {server}", "green"))
                        print(colored(
                            f"\n📩 New message on topic {message['topic']}: {message['message']}\n", "green"))

            except requests.RequestException as e:
                print(colored(f"❌ Error connecting to {server}", "red"))

            time.sleep(2)


token = None
try:
    print("--------- CONNECT TO A SERVER ---------")

    while True:

        print(colored("Type 'exit' to quit", "red"))
        user = input("Enter your username: ")
        if user == "exit":
            break
        password = input("Enter your password: ")
        server = get_random_server()
        if not server:
            print(colored("❌ No servers available!", "red"))
            continue
        response = requests.post(f"http://{server}/connect/",
                                 json={"user": user, "password": password})

        if response.status_code == 200:
            connection = response.json()
            print("Connected to server")
            print("Token:", connection["token"])
            token = connection["token"]
            stop_event.clear()
            listener_thread = threading.Thread(
                target=listen_for_messages, args=(token,), daemon=True)
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
                        queues = get_all_queues()
                        print("\nQueues:")
                        for queue in queues:
                            print(colored(queue, "yellow"))

                        print("-------------------------")
                        print("1. Create queue")
                        print("2. Send message")
                        print("3. Receive message")
                        print("4. Delete queue")
                        print("5. Suscribe to queue")
                        print("6. Unsuscribe to queue")
                        print("7. Go back")
                        print("-------------------------")
                        option = input("Select 1 option: ")

                        if option == "1":
                            queue_name = input(
                                "Enter the queue name to create: ")
                            server_address = get_random_server()
                            if not server_address:
                                continue
                            response = requests.post(f"http://{server_address}/queue/create/", json={"name": queue_name}, params={"token": token}
                                                     )
                            print("\033c", end="")
                            print(server_address, "server selected")
                            print(colored(response.json(), "yellow"))

                        elif option == "2":
                            queue_name = input("Enter the queue name: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            message = input("Enter the message: ")
                            response = requests.post(f"http://{server_address}/queue/send/",
                                                     params={"queue_name": queue_name, "message": message, "token": token})
                            print("\033c", end="")
                            print(server_address, "server selected")
                            if response.status_code == 500:
                                response = requests.post(f"http://{server_address}/queue/send/",
                                                         params={"queue_name": queue_name + '_replica', "message": message, "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "3":
                            queue_name = input(
                                "Ingrese el nombre de la cola: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            response = requests.get(f"http://{server_address}/queue/receive/",
                                                    params={"queue_name": queue_name, "token": token})
                            print("\033c", end="")
                            print(server_address, "server selected")
                            if response.status_code == 500:
                                response = requests.get(f"http://{server_address}/queue/receive/",
                                                        params={"queue_name": queue_name + '_replica', "token": token})
                            print(colored(response.json(), "green"))

                        elif option == "4":
                            queue_name = input(
                                "Ingrese el nombre de la cola: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            response = requests.delete(f"http://{server_address}/queue/",
                                                       params={"queue_name": queue_name, "token": token})
                            print("\033c", end="")
                            if response.status_code == 500:
                                response = requests.delete(f"http://{server_address}/queue/",
                                                           params={"queue_name": queue_name + '_replica', "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "5":
                            queue_name = input(
                                "Ingrese el nombre de la cola: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            response = requests.put(f"http://{server_address}/queue/subscribe/",
                                                    params={"queue_name": queue_name, "token": token})
                            print("\033c", end="")
                            if response.status_code == 500:
                                response = requests.put(f"http://{server_address}/queue/subscribe/",
                                                        params={"queue_name": queue_name + '_replica', "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "6":
                            queue_name = input(
                                "Ingrese el nombre de la cola: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            response = requests.put(f"http://{server_address}/queue/unsubscribe/",
                                                    params={"queue_name": queue_name, "token": token})
                            print("\033c", end="")
                            if response.status_code == 500:
                                response = requests.put(f"http://{server_address}/queue/unsubscribe/",
                                                        params={"queue_name": queue_name + '_replica', "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "7":
                            print("\033c", end="")
                            break

                elif option == "2":
                    listener_thread = threading.Thread(
                        target=listen_for_messages, args=(token,), daemon=True)
                    listener_thread.start()

                    while True:
                        topics = get_all_topics()
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
                            topic_name = input(
                                "Enter the topic name to create: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue

                            response = requests.post(
                                f"http://{server_address}/topic/create/",
                                json={"name": topic_name},
                                params={"token": token}
                            )
                            print("\033c", end="")
                            print(server_address, "server selected")
                            print(colored(response.json(), "yellow"))

                        elif option == "2":
                            topic_name = input("Enter the topic name: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            response = requests.put(f"http://{server_address}/topic/subscribe/",
                                                    params={"topic_name": topic_name, "token": token})

                            print("\033c", end="")
                            if response.status_code == 500:
                                response = requests.put(f"http://{server_address}/topic/subscribe/",
                                                        params={"topic_name": topic_name + '_replica', "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "3":
                            topic_name = input("Enter the topic name: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            message = input("Enter the message: ")
                            response = requests.post(f"http://{server_address}/topic/publish/",
                                                     params={"topic_name": topic_name, "message": message, "token": token})

                            print("\033c", end="")
                            if response.status_code == 500:
                                response = requests.post(f"http://{server_address}/topic/publish/",
                                                         params={"topic_name": topic_name + '_replica', "message": message, "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "4":
                            topic_name = input("Enter the topic name: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            response = requests.put(f"http://{server_address}/topic/unsubscribe/",
                                                    params={"topic_name": topic_name, "token": token})

                            print("\033c", end="")
                            if response.status_code == 500:
                                response = requests.put(f"http://{server_address}/topic/unsubscribe/",
                                                        params={"topic_name": topic_name + '_replica', "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "5":
                            topic_name = input("Enter the topic name: ")
                            server_address = get_random_server()
                            if check_servers(server_address):
                                continue
                            response = requests.delete(
                                f"http://{server_address}/topic/", params={"topic_name": topic_name, "token": token})

                            print("\033c", end="")
                            if response.status_code == 500:
                                response = requests.delete(
                                    f"http://{server_address}/topic/", params={"topic_name": topic_name + '_replica', "token": token})
                            print(colored(response.json(), "yellow"))

                        elif option == "6":
                            print("\033c", end="")
                            stop_event.set()
                            listener_thread.join()
                            stop_event.clear()
                            break
                elif option == "3":
                    remove_token(token)
                    break
                else:
                    print("\033c", end="")
                    print(colored("Invalid option", "red"))
        else:
            print("Connection failed")

except:
    remove_token(token)
