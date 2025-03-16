import requests

BASE_URL = "http://localhost:8000"

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
            f"{BASE_URL}/queue/create/", json={"name": name})
        print(response.json())
    elif option == "2":
        queue = input("Enter the queue name: ")
        message = input("Enter the message: ")
        response = requests.post(f"{BASE_URL}/queue/send/",
                                 params={"queue": queue, "message": message})
        print(response.json())
    elif option == "3":
        queue = input("Ingrese el nombre de la cola: ")
        response = requests.get(f"{BASE_URL}/queue/receive/",
                                params={"queue": queue})
        print(response.json())
    elif option == "4":
        break
