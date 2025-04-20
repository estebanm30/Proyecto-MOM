import socket
from kazoo.client import KazooClient
import os
from dotenv import load_dotenv
import sys
import time
import threading
from controllers.queue_controller import redistribute_queue
from controllers.topic_controller import redistribute_topic
from zk_utils import get_all_queues, get_queues_handled_by, get_servers, get_topics_handled_by, get_zk_client, get_server_id

zk = get_zk_client()
SERVER_ID = get_server_id()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
SERVER_PATH = f"/servers/{SERVER_ID}"

zk.ensure_path("/servers")
zk.create(SERVER_PATH, ephemeral=True, makepath=True)

print(f"✅ SERVER REGISTERED IN ZOOKEPER: {SERVER_PATH}")

fallen_servers = {}
all_known = set([])

try:
    zk.create("/leader", value=SERVER_ID.encode(), ephemeral=True)
    print(f"👑 {SERVER_ID} IS THE LEADER")
    is_leader = True
except:
    print(f"🔒 {SERVER_ID} IS NOT THE LEADER")
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
    print(f"CURRENT SERVERS: {servers}")
    all_known.update(set(servers))

    for sid in all_known:
        if sid not in servers and sid not in fallen_servers:
            fallen_servers[sid] = time.time()
            print(f"⚠️ {sid} IS NOT ONLINE!")
        elif sid in servers and sid in fallen_servers:
            print(f"✅ {sid} IS AGAIN ONLINE")
            del fallen_servers[sid]

def check_for_long_failures(threshold=10):
    now = time.time()
    for server, t in list(fallen_servers.items()):
        if now - t >= threshold:
            print(f"🛠️ {server} HAS BEEN DOWN FOR MORE THAN {threshold}s. REDISTRIBUTION IN PROGRESS...")
            rq = get_queues_handled_by(server)
            rt = get_topics_handled_by(server)
            print(f"Queues to redistribute {rq}")
            print(f"Topics to redistribute {rt}")
            redistribute_q(rq)
            redistribute_t(rt)
            print("SUCCESS REDISTRIBUTING")

            del fallen_servers[server]

def redistribute_q(rq):
    alive_servers = get_servers()
    servers_queues = {}

    for server in alive_servers:
        server_queues = get_queues_handled_by(server)
        servers_queues[server] = server_queues

    for queue in rq:
        is_replica = queue.endswith("_replica")
        base_name = queue[:-8] if is_replica else queue

        for candidate_server in alive_servers:
            assigned_queues = servers_queues[candidate_server]
            if is_replica and base_name in assigned_queues:
                continue
            if not is_replica and f"{base_name}_replica" in assigned_queues:
                continue
            
            redistribute_queue(candidate_server, queue)
            print(f"REDISTRIBUTED '{queue}' TO {candidate_server}")
            break
        else:
            print(f"⚠️ Impossible to redistribute '{queue}' — no valid servers")

def redistribute_t(rt):
    alive_servers = get_servers()
    servers_topics = {}

    for server in alive_servers:
        server_topics = get_topics_handled_by(server)
        servers_topics[server] = server_topics

    for topic in rt:
        is_replica = topic.endswith("_replica")
        base_name = topic[:-8] if is_replica else topic

        for candidate_server in alive_servers:
            assigned_topics = servers_topics[candidate_server]
            if is_replica and base_name in assigned_topics:
                continue
            if not is_replica and f"{base_name}_replica" in assigned_topics:
                continue
            
            redistribute_topic(candidate_server, topic)
            print(f"REDISTRIBUTED '{topic}' TO {candidate_server}")
            break
        else:
            print(f"⚠️ Impossible to redistribute '{topic}' — no valid servers")

def close_connection():
    if zk.exists(SERVER_PATH):
        zk.delete(SERVER_PATH)
        print(f"❌ SERVER DELETED FROM ZOOKEEPER: {SERVER_PATH}")
    zk.stop()
    zk.close()

if is_leader:
    start_failure_monitor()
