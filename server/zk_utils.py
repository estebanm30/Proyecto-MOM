from kazoo.client import KazooClient
import os
from dotenv import load_dotenv

load_dotenv()
ZOOKEEPER_ADDRESS = os.getenv("ZOOKEEPER_ADDRESS")
SERVER_ID = os.getenv("SERVER_ID")
zk = KazooClient(hosts=ZOOKEEPER_ADDRESS)
zk.start()

def get_zk_client():
    return zk

def get_server_id():
    return SERVER_ID

def get_tokens():
    tokens_path = "/tokens"
    if zk.exists(tokens_path):
        children = zk.get_children(tokens_path)
        return [f"{child}" for child in children]
    return []

def get_token_children(token):
    token_path = f"/tokens/{token}"
    if zk.exists(token_path):
        data, stat = zk.get(token_path)

        return data.decode()
    return []


def get_round_robin_replica(current_server_id):
    all_servers = ["44.194.117.112:50051",
                   "44.214.10.205:50051", "52.86.105.153:50051"]

    current_ip = current_server_id.split(
        ':')[0] if ':' in current_server_id else current_server_id
    candidates = [s for s in all_servers if not s.startswith(current_ip)]

    if not candidates:
        return None, []

    rr_path = "/round_robin_index"

    try:

        if not zk.exists(rr_path):
            zk.create(rr_path, b"0")

        current_index, _ = zk.get(rr_path)
        current_index = int(current_index.decode())
        next_index = (current_index + 1) % len(candidates)
        zk.set(rr_path, str(next_index).encode())

        return candidates[next_index], candidates
    except Exception as e:
        print(f"⚠️ ERROR IN ROUND ROBIN SELECTION: {str(e)}")

        return (candidates[0] if candidates else None), candidates
    

def get_topic_server(topic_name: str):
    path = f"/mom_topics/{topic_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode()
    path = f"/mom_topics_replicas/{topic_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode()
    return None


def get_queue_server(queue_name: str):
    path = f"/mom_queues/{queue_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode()
    path = f"/mom_queues_replicas/{queue_name}"
    if zk.exists(path):
        return zk.get(path)[0].decode()
    return None


def get_servers():
    servers_path = "/servers"
    if zk.exists(servers_path):
        return zk.get_children(servers_path)
    return []


def get_queues_handled_by(server):
    queues = []
    for queue_name in zk.get_children("/mom_queues"):
        path = f"/mom_queues/{queue_name}"
        data = zk.get(path)[0].decode()
        if data == server:
            queues.append(queue_name)
    for queue_name in zk.get_children("/mom_queues_replicas"):
        path = f"/mom_queues_replicas/{queue_name}"
        data = zk.get(path)[0].decode()
        if data == server:
            queues.append(queue_name)
    return queues

def get_topics_handled_by(server):
    topics = []
    for topic_name in zk.get_children("/mom_topics"):
        path = f"/mom_topics/{topic_name}"
        data = zk.get(path)[0].decode()
        if data == server:
            topics.append(topic_name)
    for topic_name in zk.get_children("/mom_topics_replicas"):
        path = f"/mom__topics/{topic_name}"
        data = zk.get(path)[0].decode()
        if data == server:
            topics.append(topic_name)
    return topics

def get_all_queues():
    queues_path = "/mom_queues"
    if zk.exists(queues_path):  # Verifica si el nodo existe
        return zk.get_children(queues_path)
    return []