from kazoo.client import KazooClient
import random



zk = KazooClient(hosts="localhost:2181")
zk.start()

def get_queue_server(queue_name: str):
    path = f"/mom_queues/{queue_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode() 
    return None

def get_topic_server(topic_name: str):
    path = f"/mom_topics/{topic_name}"
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


def close_connection():
    zk.stop()
    zk.close()