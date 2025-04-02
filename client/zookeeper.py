from kazoo.client import KazooClient
import random



zk = KazooClient(hosts="34.193.123.26")
zk.start()

def get_queue_server(queue_name: str):
    path = f"/mom_queues/{queue_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode() 
    return None

def get_all_queues():
    queues_path = "/mom_queues"
    if zk.exists(queues_path):  # Verifica si el nodo existe
        return zk.get_children(queues_path)
    return []

def get_all_topics():
    topics_path = "/mom_topics"
    if zk.exists(topics_path):  # Verifica si el nodo existe
        return zk.get_children(topics_path)
    return []

def get_servers():
    servers_path = "/servers"
    if zk.exists(servers_path):
        return zk.get_children(servers_path)
    return []

def get_random_server():
    servers = get_servers()
    if not servers:
        print("⚠ No servers available in Zookeeper!", "red")
        return None
    return random.choice(servers)

def remove_token(token):
    token_path = f"/tokens/{token}"
    if zk.exists(token_path):
        zk.delete(token_path)

def close_connection():
    zk.stop()
    zk.close()