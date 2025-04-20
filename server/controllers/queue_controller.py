from fastapi import HTTPException
import requests
from database import insert_queue, find_queue, find_all_queues, update_queue, delete_queue
from models import QueueModel
from utils import verify_token, check_redirect_queues
from zk_utils import zk, get_server_id, get_tokens, get_token_children, get_round_robin_replica
import mom_pb2
import mom_pb2_grpc
import grpc
from datetime import datetime

SERVER_ID = get_server_id()


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

    queue_data = {
        "name": queue.name,
        "subscribers": [],
        "messages": [],
        "pending_messages": {},
        "owner": client,
        'update_date': datetime.now()
    }

    try:
        insert_queue(queue_data)
        print(f"✅ Queue created LOCALLY on {SERVER_ID}")
    except Exception as e:
        print(f"⛔ Failed to create queue locally: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create queue")

    path = f"/mom_queues/{queue.name}"
    zk.ensure_path(path)
    zk.set(path, SERVER_ID.encode())

    replica_server, available_servers = get_round_robin_replica(SERVER_ID)

    if replica_server:
        try:
            print(
                f"🔁 [REPLICACIÓN] Seleccionado servidor {replica_server} (de disponibles: {available_servers})")
            stub = get_grpc_client(replica_server)
            response = stub.ReplicateQueue(mom_pb2.ReplicateQueueRequest(
                queue_name=queue.name + '_replica',
                owner=client
            ))
            print(
                f"✅ [REPLICACIÓN EXITOSA] en {replica_server}: {response.message}")
        except grpc.RpcError as e:
            print(
                f"⚠️ [REPLICACIÓN FALLIDA] en {replica_server}: {e.details()}")
    else:
        print("⚠️ [REPLICACIÓN] No hay servidores disponibles para replicación")

    return {"message": f"Queue created in server {SERVER_ID} and replicated in {replica_server if replica_server else 'no server'}"}


def redistribute_queue(redistribute_server, queue):
    try:
        print(f"🔁 [REPLICACIÓN] Seleccionado servidor {redistribute_server}")
        stub = get_grpc_client(redistribute_server)
        response = stub.ReplicateQueue(mom_pb2.ReplicateQueueRequest(
            queue_name=queue,
            owner='red'
        ))

        path_primary = f"/mom_queues/{queue}"
        path_replica = f"/mom_queues_replicas/{queue}"

        if zk.exists(path_primary):
            zk.set(path_primary, redistribute_server.encode())
        elif zk.exists(path_replica):
            zk.set(path_replica, redistribute_server.encode())
        else:
            print(f"⚠️ La cola '{queue}' no existe en /mom_queues ni en /mom_queues_replicas.")

        print(f"✅ [REPLICACIÓN EXITOSA] en {redistribute_server}: {response.message}")
    except grpc.RpcError as e:
        print(f"⚠️ [REPLICACIÓN FALLIDA] en {redistribute_server}: {e.details()}")


def subscribe_to_queue(queue_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect_queues(queue_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.SubscribeQueue(mom_pb2.QueueSubscriptionRequest(
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

        queue['update_date'] = datetime.now()
        update_queue(queue_name, queue)

        other_servers = ["44.194.117.112:50051", "44.214.10.205:50051",
                         "52.86.105.153:50051"]  # Cambiar dinámicamente
        for server in other_servers:
            try:
                stub = get_grpc_client(server)
                stub.ReplicateQueueSubscription(mom_pb2.ReplicateQueueSubscriptionRequest(
                    queue_name=queue_name + '_replica',
                    subscriber=user
                ))
                print(f"✅ Queue subscription replicated on {server}")
            except grpc.RpcError as e:
                print(
                    f"⚠️ Failed to replicate queue subscription on {server}: {e.details()}")

        return {"message": f"{user} subscribed to {queue_name}"}


def send_message(queue_name: str, message: str, token: str):
    verify_token(token)
    server_redirect = check_redirect_queues(queue_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.SendMessage(mom_pb2.MessageRequest(
                queue_name=queue_name, message=message, token=token))
            return {"message": response.message}
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=500, detail="gRPC error: " + e.details())
    else:
        subscriber = None
        subscriber_idx = None
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
        queue['update_date'] = datetime.now()
        update_queue(queue_name, queue)

        other_servers = ["44.194.117.112:50051",
                         "44.214.10.205:50051", "52.86.105.153:50051"]

        current_server = f"{SERVER_ID.split(':')[0]}:50051"

        servers_to_replicate = [
            server for server in other_servers if server != current_server]

        for server in servers_to_replicate:
            try:
                stub = get_grpc_client(server)
                stub.ReplicateQueueMessage(mom_pb2.ReplicateQueueMessageRequest(
                    queue_name=queue_name + '_replica',
                    message=message,
                    subscriber=subscriber,
                    current_subscriber_idx=subscriber_idx
                ))
                print(f"✅ Queue message replicated on {server}")
            except grpc.RpcError as e:
                print(
                    f"⚠️ Failed to replicate queue message on {server}: {e.details()}")

        return {"message": "Message sent"}


def receive_message(queue_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect_queues(queue_name)

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
        queue['update_date'] = datetime.now()
        update_queue(queue_name, queue)

        other_servers = ["44.194.117.112:50051", "44.214.10.205:50051",
                         "52.86.105.153:50051"]  # Cambiar dinámicamente
        for server in other_servers:
            try:
                stub = get_grpc_client(server)
                stub.ReplicateMessageDeletion(mom_pb2.ReplicateMessageDeletionRequest(
                    queue_name=queue_name + '_replica',
                    subscriber=user,
                    message=msg
                ))
                print(f"✅ Message deletion replicated on {server}")
            except grpc.RpcError as e:
                print(
                    f"⚠️ Failed to replicate message deletion on {server}: {e.details()}")

        return {"message": msg}


def delete_one_queue(queue_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect_queues(queue_name)

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

            other_servers = ["44.194.117.112:50051", "44.214.10.205:50051",
                             "52.86.105.153:50051"]  # Cambiar dinámicamente
            for server in other_servers:
                try:
                    stub = get_grpc_client(server)
                    stub.ReplicateQueueDeletion(mom_pb2.ReplicateQueueDeletionRequest(
                        queue_name=queue_name + '_replica',
                        owner=client,
                        subscribers=queue["subscribers"]
                    ))
                    print(f"✅ Queue deletion replicated on {server}")
                except grpc.RpcError as e:
                    print(
                        f"⚠️ Failed to replicate queue deletion on {server}: {e.details()}")

            delete_queue(queue_name)
            path = f"/mom_queues/{queue_name}"
            if zk.exists(path):
                zk.delete(path)
            if queue_name.endswith('_replica'):
                path = f"/mom_queues/{queue_name.replace('_replica', '')}"
                if zk.exists(path):
                    zk.delete(path)
                path = f"/mom_queues_replicas/{queue_name}"
                if zk.exists(path):
                    zk.delete(path)
            return {"message": "Queue deleted"}
        else:
            return {"message": "You cannot delete this queue"}


def unsubscribe_to_queue(queue_name: str, token: str):
    verify_token(token)
    server_redirect = check_redirect_queues(queue_name)

    if server_redirect is not None:
        try:
            client = get_grpc_client(server_redirect)
            response = client.UnsubscribeQueue(mom_pb2.QueueSubscriptionRequest(
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
        queue["subscribers"].remove(user)
        queue['update_date'] = datetime.now()
        update_queue(queue_name, queue)

        other_servers = ["44.194.117.112:50051", "44.214.10.205:50051",
                         "52.86.105.153:50051"]  # Cambiar dinámicamente
        for server in other_servers:
            try:
                stub = get_grpc_client(server)
                stub.ReplicateQueueUnsubscription(mom_pb2.ReplicateQueueUnsubscriptionRequest(
                    queue_name=queue_name + '_replica',
                    subscriber=user
                ))
                print(f"✅ Queue unsubscription replicated on {server}")
            except grpc.RpcError as e:
                print(
                    f"⚠️ Failed to replicate queue unsubscription on {server}: {e.details()}")

        return {"message": f"{user} unsubscribed from {queue_name}"}


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
            queue['update_date'] = datetime.now()
            update_queue(queue['name'], queue)
    queues = find_all_queues()
    for queue in queues:
        cont = 0
        for pending_message in queue['pending_messages'].values():
            if len(pending_message) > 0:
                cont += 1
        if cont == 0:
            queue['messages'] = []
            queue['update_date'] = datetime.now()
            update_queue(queue['name'], queue)
            """
            #Va acá o en receive_message?
            
            other_servers = ["44.194.117.112:50051", "44.214.10.205:50051", "52.86.105.153:50051"]  # Cambiar dinámicamente
            for server in other_servers:
                try:
                    stub = get_grpc_client(server)
                    stub.ReplicateMessageDeletion(mom_pb2.ReplicateMessageDeletionRequest(
                        queue_name=queue_name,
                        subscriber=user,
                        message=msg
                    ))
                    print(f"✅ Message deletion replicated on {server}")
                except grpc.RpcError as e:
                    print(f"⚠️ Failed to replicate message deletion on {server}: {e.details()}")
            """
    return {"messages": messages}
