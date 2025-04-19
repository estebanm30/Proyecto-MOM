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

print(f"✅ SERVER REGISTERED IN ZOOKEPER: {SERVER_PATH}")


fallen_servers = {}
all_known = set([])

try:
    zk.create("/leader", value=SERVER_ID.encode(), ephemeral=True)
    print(f"👑 {SERVER_ID} es el líder.")
    is_leader =  True
except:
    print(f"🔒 {SERVER_ID} no es el líder.")
    is_leader = False

def start_failure_monitor(interval=10):
    def monitor():
        while True:
            check_for_long_failures()
            time.sleep(interval)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()


@zk.ChildrenWatch("/servers")
def watch_servers(servers):
    print(f"Lista de servidores actuales: {servers}")
    all_known.add(set(servers))

    print(f"all known{all_known}")

    for sid in all_known:
        print(f"Comprobando servidor: {sid}")
        if sid not in servers and sid not in fallen_servers:
            fallen_servers[sid] = time.time()
            print(f"⚠️ {sid} cayó a las {fallen_servers[sid]}")

        elif sid in servers and sid in fallen_servers:
            print(f"✅ {sid} volvió luego de {time.time() - fallen_servers[sid]}s")
            del fallen_servers[sid]

def check_for_long_failures(threshold=60):
    while True:
        now = time.time()
        to_remove = []
        for server, t in fallen_servers.items():
            if now - t >= threshold:
                print(f"🛠️ {server} ha estado caído más de {threshold}s. Redistribuyendo recursos...")
                # Aquí haces la redistribución
                to_remove.append(server)

        for s in to_remove:
            del fallen_servers[s]

        time.sleep(5)

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


if is_leader:
    t = threading.Thread(target=check_for_long_failures, daemon=True)
    t.start()


