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
            print("1. Crear cola")
            print("2. Enviar mensaje")
            print("3. Recibir mensaje")
            print("4. Salir")
            print("-------------------------")

            option = input("Seleccione una opción: ")
                
            if option == "1":
                name = input("Enter the queue name to create: ")
                response = requests.post(
                    f"{BASE_URL}/queue/create/", json={"name": name}, params={"token": token})
                print(response.json())
            elif option == "2":
                queue = input("Enter the queue name: ")
                message = input("Enter the message: ")
                response = requests.post(f"{BASE_URL}/queue/send/",params={"queue": queue, "message": message, "token": token})
                print(response.json())
            elif option == "3":
                queue = input("Ingrese el nombre de la cola: ")
                response = requests.get(f"{BASE_URL}/queue/receive/",
                                        params={"queue": queue, "token": token})
                print(response.json())
            elif option == "4":
                break
    else:
        print("Connection failed")
