from fastapi import HTTPException, BackgroundTasks
import requests
from database import insert_queue, find_queue, find_all_queues, update_queue, delete_queue
from models import QueueModel
from utils import check_redirect, verify_token
from zookeeper import zk, SERVER_ID, get_tokens, get_token_children
import mom_pb2
import mom_pb2_grpc
import grpc


def get_queues(token: str):
    verify_token(token)
    queues = find_all_queues()
    names = []
    for queue in queues:
        names.append(queue["name"])
    return names


def get_grpc_client(server_address):
    print('------------------- Using gRPC client',
          server_address, '---------------------')
    newServer_address = f"{server_address[:server_address.find(':')]}:50051"
    channel = grpc.insecure_channel(newServer_address)
    return mom_pb2_grpc.QueueServiceStub(channel)


def create_queue(queue: QueueModel, token: str):
    verify_token(token)
    client = get_token_children(token)

    if not client:
        raise HTTPException(status_code=401, detail="Invalid token")

    if find_queue(queue.name):
        raise HTTPException(status_code=400, detail="Queue already exists")

    insert_queue({"name": queue.name, "subscribers": [],
                 "messages": [], "pending_messages": {}, "owner": client})

    path = f"/mom_queues/{queue.name}"
    zk.ensure_path(path)
    zk.set(path, SERVER_ID.encode())

    print(list(find_all_queues()))
    return {"message": "Queue created"}


def subscribe_to_queue(queue_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect(queue_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.SubscribeQueue(mom_pb2.SubscriptionRequest(
                queue_name=queue_name, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        user = get_token_children(token)
        queue = find_queue(queue_name)
        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")
        if user in queue["subscribers"]:
            raise HTTPException(status_code=400, detail="Already subscribed")
        else:
            queue["subscribers"].append(user)
            queue["pending_messages"][user] = []

        update_queue(queue_name, queue)
        return {"message": f"{user} subscribed to {queue_name}"}


def send_message(queue_name: str, message: str, token: str, background_tasks: BackgroundTasks):
    verify_token(token)
    server_redirect = check_redirect(queue_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.SendMessage(mom_pb2.MessageRequest(
                queue_name=queue_name, message=message, token=token , background_tasks=background_tasks))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        queue = find_queue(queue_name)
        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        if not queue["subscribers"]:
            queue["messages"].append(message)
        else:
            if "current_subscriber_idx" not in queue:
                queue["current_subscriber_idx"] = 0

            subscriber_idx = queue["current_subscriber_idx"]
            subscriber = queue["subscribers"][subscriber_idx]

            queue["pending_messages"][subscriber].append(message)

            queue["current_subscriber_idx"] = (
                subscriber_idx + 1) % len(queue["subscribers"])

        update_queue(queue_name, queue)
        return {"message": "Message sent"}


def receive_message(queue_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect(queue_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.ReceiveMessage(mom_pb2.QueueRequest(
                queue_name=queue_name, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        user = get_token_children(token)
        queue = find_queue(queue_name)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        if user not in queue["subscribers"]:
            raise HTTPException(
                status_code=403, detail="Not subscribed to this queue")

        if not queue["pending_messages"][user]:
            raise HTTPException(status_code=404, detail="No pending messages")

        current_idx = queue.get("current_subscriber_idx", 0)
        next_subscriber = queue["subscribers"][current_idx]

        if user != next_subscriber:
            raise HTTPException(
                status_code=403,
                detail="Not your turn (Round Robin in progress)"
            )

        msg = queue["pending_messages"][user].pop(0)

        queue["current_subscriber_idx"] = (
            current_idx + 1) % len(queue["subscribers"])
        update_queue(queue_name, queue)

        return {"message": msg}


def delete_one_queue(queue_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect(queue_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.DeleteQueue(mom_pb2.QueueRequest(
                queue_name=queue_name, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        client = get_token_children(token)
        queue = find_queue(queue_name)
        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")
        if queue["owner"] == client:
            delete_queue(queue_name)
            path = f"/mom_queues/{queue_name}"
            if zk.exists(path):
                zk.delete(path)
            return {"message": "Queue deleted"}
        else:
            return {"message": "You cannot delete this queue"}


def get_messages_queue(token: str):
    verify_token(token)
    user = get_token_children(token)
    queue = find_all_queues()
    messages = []
    for queue in queues:
        if user in queue['subscribers'] and queue['pending_messages'][user]:
            messages.append(
                {"queue": queue['name'], "message": queue['pending_messages'][user]})
            queue['pending_messages'][user] = []
            update_queue(queue['name'], queue)
    queues = find_all_queues()
    for queue in queues:
        cont = 0
        for pending_message in queue['pending_messages'].values():
            if len(pending_message) > 0:
                cont += 1
        if cont == 0:
            queue['messages'] = []
            update_queue(queue['name'], queue)

    return {"messages": messages}
