import socket
from kazoo.client import KazooClient
import os
from dotenv import load_dotenv
import sys
load_dotenv()
ZOOKEEPER_ADDRESS = os.getenv("ZOOKEEPER_ADDRESS")
SERVER_ID = os.getenv("SERVER_ID")
zk = KazooClient(hosts=ZOOKEEPER_ADDRESS)
zk.start()  

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
SERVER_PATH = f"/servers/{SERVER_ID}"

zk.ensure_path("/servers")
zk.create(SERVER_PATH, ephemeral=True, makepath=True)

print(f"✅ Server registrado en Zookeeper: {SERVER_PATH}")


def get_tokens():
    tokens_path = "/tokens"
    if zk.exists(tokens_path):
        children = zk.get_children(tokens_path)
        return [f"{child}" for child in children]
    return []

def get_topic_server(topic_name: str):
    path = f"/mom_topics/{topic_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode() 
    return None

def get_queue_server(queue_name: str):
    path = f"/mom_queues/{queue_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode() 
    return None

def get_token_children(token):
    token_path = f"/tokens/{token}"
    if zk.exists(token_path):
        data, stat = zk.get(token_path)

        return data.decode()
    return []


def close_connection():
    if zk.exists(SERVER_PATH):
        zk.delete(SERVER_PATH)
        print(f"❌ Server eliminado de Zookeeper: {SERVER_PATH}")
    zk.stop()
    zk.close()

def get_active_servers(exclude_current=True):
    """Obtiene todos los servidores activos excluyendo el actual"""
    servers = []
    if zk.exists("/servers"):
        current_server = SERVER_ID  # Formato "ip:8000"
        for server_id in zk.get_children("/servers"):
            # Obtenemos el valor almacenado (ip:puerto_http)
            data, _ = zk.get(f"/servers/{server_id}")
            server_address = data.decode()
            
            # Excluir el servidor actual
            if exclude_current and server_address == current_server:
                continue
                
            # Convertir a dirección gRPC (misma IP, puerto 50051)
            ip = server_address.split(":")[0]
            servers.append(f"{ip}:50051")
    return servers