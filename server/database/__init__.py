from fastapi import HTTPException
import mom_pb2_grpc
import mom_pb2
from .connection import get_db
from .queues_queries import insert_queue, find_queue, find_all_queues, update_queue, delete_queue
from .topics_queries import insert_topic, find_all_topics, find_topic, update_topic, delete_topic
from .clients_queries import delete_client, update_client, find_client, find_all_clients
import grpc
from zookeeper import get_queue_server, get_topic_server


def get_grpc_client(server_address):
    print('------------------- Using gRPC client',
          server_address, '---------------------')
    newServer_address = f"{server_address[:server_address.find(':')]}:50051"
    channel = grpc.insecure_channel(newServer_address)
    return mom_pb2_grpc.OnBootingStub(channel)


queues = find_all_queues()
topics = find_all_topics()

for queue in queues:
    if queue['name'].find('replica') != -1:
        name = queue['name'] + '_replica'
        print(name)
        server_redirect = get_queue_server(name)
    else:
        name = queue['name'].replace('_replica', '')
        print(name)
        server_redirect = get_queue_server(name)
    try:
        client = get_grpc_client(server_redirect)
        response = client.updateTopic(
            mom_pb2.ReplicateQueueRequest(name=name, owner=queue['owner']))

        if queue['update_date'] < response['update_date']:
            update_queue(queue['name'], response['subscribers'], response['messages'],
                         response['pending_messages'], response['owner'], response['update_date'])
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Server not online!")


for topic in topics:
    if topic['name'].find('replica') != -1:
        server_redirect = get_topic_server(topic['name'] + '_replica')
        name = queue['name'] + '_replica'
    else:
        server_redirect = get_topic_server(topic['name'])
        name = queue['name']
    try:
        client = get_grpc_client(server_redirect)
        response = client.updateTopic(
            mom_pb2.ReplicateTopicRequest(name=name, owner=topic['owner']))

        if queue['update_date'] < response['update_date']:
            update_topic(topic['name'], response['subscribers'], response['messages'],
                         response['pending_messages'], response['owner'], response['update_date'])
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Server not online!")

__all__ = ["insert_queue",
           "find_queue", "find_all_queues", "update_queue", "delete_queue", "insert_topic", "find_all_topics", "find_topic", "update_topic", "delete_topic", "find_all_clients", "find_client", "update_client", "delete_client"]
