from fastapi import HTTPException
import mom_pb2_grpc
import mom_pb2
from .connection import get_db
from .queues_queries import insert_queue, find_queue, find_all_queues, update_queue, delete_queue
from .topics_queries import insert_topic, find_all_topics, find_topic, update_topic, delete_topic
from .clients_queries import delete_client, update_client, find_client, find_all_clients
import grpc
from zookeeper import get_queue_server, get_topic_server, get_servers, zk


def get_grpc_client(server_address):
    print('------------------- Using gRPC client',
          server_address, '---------------------')
    newServer_address = f"{server_address[:server_address.find(':')]}:50051"
    channel = grpc.insecure_channel(newServer_address)
    return mom_pb2_grpc.OnBootingStub(channel)


queues = find_all_queues()
topics = find_all_topics()
online_servers = get_servers()

for queue in queues:
    if queue['name'].find('replica') == -1:
        name = queue['name'] + '_replica'
        server_redirect = get_queue_server(name)
    else:
        name = queue['name'].replace('_replica', '')
        print(name)
        server_redirect = get_queue_server(name)
        try:
            path = f"/mom_queues/{name}"
            if zk.exists(path):
                zk.delete(path)
        except Exception as e:
            print(f"Error deleting queue from ZooKeeper: {e}")
    if not server_redirect:
        delete_queue(queue['name'])
        try:
            path = f"/mom_queues_replicas/{queue['name']}"
            if zk.exists(path):
                zk.delete(path)
        except Exception as e:
            print(f"Error deleting queue from ZooKeeper: {e}")
        try:
            path = f"/mom_queues/{queue['name']}"
            if zk.exists(path):
                zk.delete(path)
        except Exception as e:
            print(f"Error deleting queue from ZooKeeper: {e}")
        continue
    try:
        if server_redirect[:server_redirect.find(':')]+':8000' in online_servers[:]:
            client = get_grpc_client(server_redirect)
            response = client.updateQueues(
                mom_pb2.ReplicateQueueRequest(queue_name=name, owner=queue['owner']))

            if queue['update_date'] < response.update_date.ToDatetime():
                pending = {}
                for k, v in response.pending_messages.items():
                    pending[k] = list(v.messages)
                queue = {
                    'name': queue['name'],
                    'subscribers': list(response.subscribers),
                    'messages': list(response.messages),
                    'pending_messages': pending,
                    'owner': response.owner,
                    'update_date': response.update_date.ToDatetime()
                }
                update_queue(queue['name'], queue)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Server not online!")


for topic in topics:
    if topic['name'].find('replica') == -1:
        name = topic['name'] + '_replica'
        server_redirect = get_topic_server(name)
    else:
        name = topic['name'].replace('_replica', '')
        server_redirect = get_topic_server(name)
    if not server_redirect:
        delete_topic(topic['name'])
        try:
            path = f"/mom_topics_replicas/{topic['name']}"
            if zk.exists(path):
                zk.delete(path)
        except Exception as e:
            print(f"Error deleting queue from ZooKeeper: {e}")
        try:
            path = f"/mom_topics/{topic['name']}"
            if zk.exists(path):
                zk.delete(path)
        except Exception as e:
            print(f"Error deleting queue from ZooKeeper: {e}")
        continue
    try:
        if server_redirect[:server_redirect.find(':')]+':8000' in online_servers[:]:
            client = get_grpc_client(server_redirect)
            response = client.updateTopic(
                mom_pb2.ReplicateTopicRequest(topic_name=name, owner=topic['owner']))

            if topic['update_date'] < response.update_date.ToDatetime():
                pending = {}
                for k, v in response.pending_messages.items():
                    pending[k] = list(v.messages)
                topic = {
                    'name': topic['name'],
                    'subscribers': list(response.subscribers),
                    'messages': list(response.messages),
                    'pending_messages': pending,
                    'owner': response.owner,
                    'update_date': response.update_date.ToDatetime()
                }
                update_topic(topic['name'], topic)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Server not online!")

__all__ = ["insert_queue",
           "find_queue", "find_all_queues", "update_queue", "delete_queue", "insert_topic", "find_all_topics", "find_topic", "update_topic", "delete_topic", "find_all_clients", "find_client", "update_client", "delete_client"]
