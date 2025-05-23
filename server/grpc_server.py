from google.protobuf.timestamp_pb2 import Timestamp
import grpc
from concurrent import futures
import time
import mom_pb2
import mom_pb2_grpc
import threading
from database import insert_topic, find_all_topics, find_topic, update_topic, delete_topic, find_queue, insert_queue, update_queue, delete_queue, find_all_queues
from controllers.topic_controller import (
    publish_message, subscribe_to_topic, unsubscribe_from_topic, delete_one_topic
)
from controllers.queue_controller import subscribe_to_queue, send_message, receive_message, delete_one_queue, unsubscribe_to_queue
from fastapi import HTTPException, BackgroundTasks
from zookeeper import get_zk_client, zk, SERVER_ID
from datetime import datetime


class MOMService(mom_pb2_grpc.TopicServiceServicer):
    def __init__(self):
        self.zk = get_zk_client()

    def Publish(self, request, context):
        try:
            background_tasks = BackgroundTasks()
            response = publish_message(
                request.topic_name, request.message, request.token, background_tasks)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def Subscribe(self, request, context):
        try:
            response = subscribe_to_topic(request.topic_name, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def Unsubscribe(self, request, context):
        try:
            response = unsubscribe_from_topic(
                request.topic_name, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def DeleteTopic(self, request, context):
        try:
            response = delete_one_topic(request.topic_name, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def ReplicateTopic(self, request, context):
        try:
            if not find_topic(request.topic_name):
                insert_topic({
                    "name": request.topic_name,
                    "subscribers": [],
                    "messages": [],
                    "pending_messages": {},
                    "owner": request.owner,
                    'update_date': datetime.now()
                })
                if request.topic_name.endswith("_replica"):
                    path = f"/mom_topics_replicas/{request.topic_name}"
                    zk.ensure_path(path)
                    zk.set(path, SERVER_ID.encode())

            return mom_pb2.Response(message=f"Replicated topic {request.topic_name}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Replication failed")

    def ReplicateSubscription(self, request, context):
        try:
            topic = find_topic(request.topic_name)
            if topic:
                if request.subscriber not in topic['subscribers']:
                    topic['subscribers'].append(request.subscriber)
                    topic['pending_messages'][request.subscriber] = []
                    topic['update_date'] = datetime.now()
                    update_topic(request.topic_name, topic)
                return mom_pb2.Response(message=f"Replicated subscription to {request.topic_name} for {request.subscriber}")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Topic not found")
                return mom_pb2.Response(message="Topic not found")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Subscription replication failed")

    def ReplicateMessage(self, request, context):
        try:
            topic = find_topic(request.topic_name)
            if topic:

                topic['messages'].append(request.message)

                for subscriber in request.subscribers:
                    if subscriber in topic['pending_messages']:
                        topic['pending_messages'][subscriber].append(
                            request.message)
                    else:
                        topic['pending_messages'][subscriber] = [
                            request.message]
                topic['update_date'] = datetime.now()
                update_topic(request.topic_name, topic)
                return mom_pb2.Response(message=f"Replicated message in {request.topic_name}")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Topic not found")
                return mom_pb2.Response(message="Topic not found")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Message replication failed")

    def ReplicateUnsubscription(self, request, context):
        try:
            topic = find_topic(request.topic_name)
            if topic:
                if request.subscriber in topic['subscribers']:
                    topic['subscribers'].remove(request.subscriber)
                    topic['pending_messages'].pop(request.subscriber, None)
                    topic['update_date'] = datetime.now()
                    update_topic(request.topic_name, topic)
                return mom_pb2.Response(message=f"Replicated unsubscription from {request.topic_name} for {request.subscriber}")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Topic not found")
                return mom_pb2.Response(message="Topic not found")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Unsubscription replication failed")

    def ReplicateTopicDeletion(self, request, context):
        try:
            topic = find_topic(request.topic_name)
            if topic:

                topic['messages'].append(request.last_message)
                for subscriber in request.subscribers:
                    if subscriber in topic['pending_messages']:
                        topic['pending_messages'][subscriber].append(
                            request.last_message)
                topic['update_date'] = datetime.now()
                update_topic(request.topic_name, topic)
                time.sleep(2)

                delete_topic(request.topic_name)
                try:

                    path = f"/mom_topics_replicas/{request.topic_name}"
                    if zk.exists(path):
                        zk.delete(path)
                except Exception as e:
                    print(f"Error deleting topic from ZooKeeper: {e}")

                return mom_pb2.Response(message=f"Replicated deletion of topic {request.topic_name}")
            else:
                return mom_pb2.Response(message=f"Topic {request.topic_name} not found, nothing to delete")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Topic deletion replication failed")


class QueueServiceHandler(mom_pb2_grpc.QueueServiceServicer):

    def SubscribeQueue(self, request, context):
        try:
            response = subscribe_to_queue(request.queue_name, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def SendMessage(self, request, context):
        try:
            response = send_message(
                request.queue_name, request.message, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def ReceiveMessage(self, request, context):
        try:
            response = receive_message(request.queue_name, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def DeleteQueue(self, request, context):
        try:
            response = delete_one_queue(request.queue_name, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def UnsubscribeQueue(self, request, context):
        try:
            response = unsubscribe_to_queue(request.queue_name, request.token)
            return mom_pb2.Response(message=response["message"])
        except HTTPException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.detail)
            return mom_pb2.Response(message="Error")

    def ReplicateQueue(self, request, context):
        try:
            if not find_queue(request.queue_name):
                insert_queue({
                    "name": request.queue_name,
                    "subscribers": [],
                    "messages": [],
                    "pending_messages": {},
                    "owner": request.owner,
                    'update_date': datetime.now()
                })
                if request.queue_name.endswith("_replica"):
                    path = f"/mom_queues_replicas/{request.queue_name}"
                    zk.ensure_path(path)
                    zk.set(path, SERVER_ID.encode())



            return mom_pb2.Response(message=f"Replicated queue {request.queue_name}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Queue replication failed")

    def ReplicateQueueSubscription(self, request, context):
        try:
            queue = find_queue(request.queue_name)
            if queue:
                if request.subscriber not in queue['subscribers']:
                    queue['subscribers'].append(request.subscriber)
                    queue['pending_messages'][request.subscriber] = []
                    queue['update_date'] = datetime.now()
                    update_queue(request.queue_name, queue)
                return mom_pb2.Response(message=f"Replicated subscription to queue {request.queue_name} for {request.subscriber}")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Queue not found")
                return mom_pb2.Response(message="Queue not found")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Queue subscription replication failed")

    def ReplicateQueueMessage(self, request, context):
        try:
            queue = find_queue(request.queue_name)
            if queue:
                if request.subscriber:
                    if request.subscriber in queue['pending_messages']:
                        queue['pending_messages'][request.subscriber].append(
                            request.message)
                    else:
                        queue['pending_messages'][request.subscriber] = [
                            request.message]
                else:
                    queue['messages'].append(request.message)

                if request.current_subscriber_idx >= 0:
                    queue['current_subscriber_idx'] = request.current_subscriber_idx
                queue['update_date'] = datetime.now()
                update_queue(request.queue_name, queue)
                return mom_pb2.Response(message=f"Replicated message in queue {request.queue_name}")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Queue not found")
                return mom_pb2.Response(message="Queue not found")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Queue message replication failed")

    def ReplicateQueueUnsubscription(self, request, context):
        try:
            queue = find_queue(request.queue_name)
            if queue:
                if request.subscriber in queue['subscribers']:
                    queue['subscribers'].remove(request.subscriber)
                    queue['pending_messages'].pop(request.subscriber, None)
                    queue['update_date'] = datetime.now()
                    update_queue(request.queue_name, queue)
                return mom_pb2.Response(message=f"Replicated unsubscription from queue {request.queue_name} for {request.subscriber}")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Queue not found")
                return mom_pb2.Response(message="Queue not found")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Queue unsubscription replication failed")

    def ReplicateQueueDeletion(self, request, context):
        try:
            queue = find_queue(request.queue_name)
            if queue:

                delete_queue(request.queue_name)
                try:
                    path = f"/mom_queues_replicas/{request.queue_name}"
                    if zk.exists(path):
                        zk.delete(path)
                except Exception as e:
                    print(f"Error deleting queue from ZooKeeper: {e}")

                return mom_pb2.Response(message=f"Replicated deletion of queue {request.queue_name}")
            else:
                return mom_pb2.Response(message=f"Queue {request.queue_name} not found, nothing to delete")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Queue deletion replication failed")

    def ReplicateMessageDeletion(self, request, context):
        try:
            queue = find_queue(request.queue_name)
            if queue:
                if request.subscriber in queue['pending_messages']:

                    if request.message in queue['pending_messages'][request.subscriber]:
                        queue['pending_messages'][request.subscriber].remove(
                            request.message)
                        queue['update_date'] = datetime.now()
                        update_queue(request.queue_name, queue)
                return mom_pb2.Response(message=f"Replicated message deletion from queue {request.queue_name} for {request.subscriber}")
            else:
                return mom_pb2.Response(message=f"Queue {request.queue_name} not found")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mom_pb2.Response(message="Message deletion replication failed")


class OnBooting(mom_pb2_grpc.OnBootingServicer):
    def updateTopic(self, request, context):
        topic = find_topic(request.topic_name)
        if not topic:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Topic not found")
            return mom_pb2.Topic()

        ts = Timestamp()
        ts.FromDatetime(topic['update_date'])

        return mom_pb2.Topic(
            name=topic['name'],
            subscribers=topic['subscribers'],
            messages=topic['messages'],
            pending_messages={
                k: mom_pb2.MessageList(messages=v)
                for k, v in topic['pending_messages'].items()
            },
            owner=topic['owner'],
            update_date=ts
        )

    def updateQueues(self, request, context):
        queue = find_queue(request.queue_name)
        if not queue:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Queue not found")
            return mom_pb2.Queue()

        ts = Timestamp()
        ts.FromDatetime(queue['update_date'])

        return mom_pb2.Queue(
            name=queue['name'],
            subscribers=queue['subscribers'],
            messages=queue['messages'],
            pending_messages={
                k: mom_pb2.MessageList(messages=v)
                for k, v in queue['pending_messages'].items()
            },
            owner=queue['owner'],
            update_date=ts
        )


def serve():
    print("GRPC RUNNING...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    mom_pb2_grpc.add_TopicServiceServicer_to_server(MOMService(), server)
    mom_pb2_grpc.add_QueueServiceServicer_to_server(
        QueueServiceHandler(), server)
    mom_pb2_grpc.add_OnBootingServicer_to_server(OnBooting(), server)
    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"🚀 gRPC server running on port {port}")

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("🛑 gRPC server shutted down")
        server.stop(0)


def start_grpc_server():
    grpc_thread = threading.Thread(target=serve, daemon=True)
    grpc_thread.start()
