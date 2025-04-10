import time
import grpc
from fastapi import HTTPException, BackgroundTasks
from database import insert_topic, find_all_topics, find_topic, update_topic, delete_topic
from models import TopicModel
from utils import verify_token, check_redirect
from zookeeper import zk, SERVER_ID, get_token_children, get_topic_server
import mom_pb2
import mom_pb2_grpc



def get_topics(token: str):
    verify_token(token)
    topics = find_all_topics()
    names = []
    for topic in topics:
        names.append(topic["name"])
    return names


def create_topic(topic: TopicModel, token: str):
    verify_token(token)
    client = get_token_children(token)
    if find_topic(topic.name):
        raise HTTPException(status_code=400, detail="Topic already exists")
    insert_topic({"name": topic.name, "subscribers": [],
                 "messages": [], "pending_messages": {}, "owner": client})

    path = f"/mom_topics/{topic.name}"
    zk.ensure_path(path)
    zk.set(path, SERVER_ID.encode())

    return {"message": "Topic created"}


def get_grpc_client(server_address):
    print('------------------- Using gRPC client',
          server_address, '---------------------')
    newServer_address = f"{server_address[:server_address.find(':')]}:50051"
    channel = grpc.insecure_channel(newServer_address)
    return mom_pb2_grpc.TopicServiceStub(channel)


def subscribe_to_topic(topic_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect(topic_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.Subscribe(mom_pb2.SubscriptionRequest(
                topic_name=topic_name, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        user = get_token_children(token)
        topic = find_topic(topic_name)
        if user in topic['subscribers']:
            raise HTTPException(status_code=400, detail="Already subscribed")
        else:
            topic['subscribers'].append(user)
            topic['pending_messages'][user] = []

        update_topic(topic_name, topic)
        return {"message": f"{user} subscribed to {topic_name}"}


def unsubscribe_from_topic(topic_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect(topic_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.Unsubscribe(
                mom_pb2.SubscriptionRequest(topic_name=topic_name, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        user = get_token_children(token)
        topic = find_topic(topic_name)
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        if user not in topic['subscribers']:
            raise HTTPException(status_code=400, detail="Not subscribed")
        else:
            topic['subscribers'].remove(user)
            topic['pending_messages'].pop(user, None)
        update_topic(topic_name, topic)
        return {"message": f"{user} unsubscribed from {topic_name}"}


def publish_message(topic_name: str, message: str, token: str, background_tasks: BackgroundTasks):
    verify_token(token)
    server_redirect = check_redirect(topic_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.Publish(mom_pb2.PublishRequest(
                topic_name=topic_name, message=message, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        topic = find_topic(topic_name)
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")

        topic['messages'].append(message)
        for subscriber in topic['subscribers']:
            topic['pending_messages'][subscriber].append(message)

        update_topic(topic_name, topic)
        return {"message": f"Message published to {len(topic['subscribers'])} subscribers"}


def delete_one_topic(topic_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect(topic_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.DeleteTopic(
                mom_pb2.DeleteRequest(topic_name=topic_name, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        client = get_token_children(token)
        topic = find_topic(topic_name)
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        if topic["owner"] == client:
            message = f"The topic {topic_name} has been eliminated by the owner"
            topic['messages'].append(message)
            for subscriber in topic['subscribers']:
                topic['pending_messages'][subscriber].append(message)
            update_topic(topic_name, topic)
            time.sleep(2)
            delete_topic(topic_name)
            path = f"/mom_topics/{topic_name}"
            if zk.exists(path):
                zk.delete(path)
        else:
            return {"message": "You cannot delete this topic"}
        return {"message": "Topic deleted"}


def get_messages(token: str):
    verify_token(token)
    user = get_token_children(token)
    topics = find_all_topics()
    messages = []
    for topic in topics:
        if user in topic['subscribers'] and topic['pending_messages'][user]:
            messages.append(
                {"topic": topic['name'], "message": topic['pending_messages'][user]})
            topic['pending_messages'][user] = []
            update_topic(topic['name'], topic)
    topics = find_all_topics()
    for topic in topics:
        cont = 0
        for pending_message in topic['pending_messages'].values():
            if len(pending_message) > 0:
                cont += 1
        if cont == 0:
            topic['messages'] = []
            update_topic(topic['name'], topic)

    return {"messages": messages}
