import socket
from kazoo.client import KazooClient
import os
from dotenv import load_dotenv
import sys
import time
import threading

load_dotenv()
ZOOKEEPER_ADDRESS = os.getenv("ZOOKEEPER_ADDRESS")
SERVER_ID = os.getenv("SERVER_ID")
zk = KazooClient(hosts=ZOOKEEPER_ADDRESS)
zk.start()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
SERVER_PATH = f"/servers/{SERVER_ID}"

zk.ensure_path("/servers")
zk.create(SERVER_PATH, ephemeral=True, makepath=True)


def check_for_long_failures_loop():
    while True:
        check_for_long_failures()
        time.sleep(10)


threading.Thread(target=check_for_long_failures_loop, daemon=True).start()

print(f"✅ SERVER REGISTERED IN ZOOKEPER: {SERVER_PATH}")


fallen_servers = {}

@zk.ChildrenWatch("/servers")
def watch_servers(servers):
    current_servers = set(servers)
    all_known = set(fallen_servers.keys()).union(current_servers)

    for server in all_known:
        if server not in current_servers and server not in fallen_servers:
            fallen_servers[server] = time.time()
            print(f"⚠️ {server} FAILED AT {fallen_servers[server]}")

        elif server in current_servers and server in fallen_servers:
            print(f"✅ {server} IS BACK AFTER {time.time() - fallen_servers[server]}s")
            del fallen_servers[server]

def check_for_long_failures(threshold=60):
    now = time.time()
    for server, t in fallen_servers.items():
        if now - t >= threshold:
            print(f"🛠️ {server} HAS BEEN DOWN FOR MORE THAN {threshold}s. BALANCING...")
            #REDISTRIBUTING
            del fallen_servers[server]

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


def get_servers():
    servers_path = "/servers"
    if zk.exists(servers_path):
        return zk.get_children(servers_path)
    return []


def get_zk_client():
    return zk


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
        print(f"⚠️ Error en round robin selection: {str(e)}")

        return (candidates[0] if candidates else None), candidates

def check_for_long_failures(threshold=60):
    now = time.time()
    for server, t in fallen_servers.items():
        if now - t >= threshold:
            print(f"🛠️ {server} HAS BEEN DOWN FOR MORE THAN {threshold}s. BALANCING...")
            # Aquí puedes llamar a tu lógica de redistribución

