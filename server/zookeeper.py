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

def get_zk_client():
    return zk

# zookeeper.py (agregar estas funciones)
def get_next_replica_server(current_server_id):
    """Obtiene el próximo servidor para replicación round robin"""
    servers = get_active_servers()
    if not servers:
        return None
    
    # Filtrar el servidor actual
    candidates = [s for s in servers if s != current_server_id]
    if not candidates:
        return None
    
    # Obtener o crear el índice de round robin
    rr_path = "/round_robin_index"
    if not zk.exists(rr_path):
        zk.create(rr_path, b"0")
    
    # Incrementar el índice atómicamente
    current_index, _ = zk.get(rr_path)
    current_index = int(current_index.decode())
    next_index = (current_index + 1) % len(candidates)
    zk.set(rr_path, str(next_index).encode())
    
    return candidates[next_index]

def get_server_address(server_id):
    """Obtiene la dirección de un servidor por su ID"""
    path = f"/servers/{server_id}"
    if zk.exists(path):
        data, _ = zk.get(path)
        return data.decode() + ":50051"  # Asumiendo puerto fijo 50051
    return None