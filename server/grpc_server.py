import grpc
from concurrent import futures
import time
import mom_pb2
import mom_pb2_grpc
import threading
from database import insert_topic, find_all_topics, find_topic, update_topic, delete_topic
from controllers.topic_controller import (
    publish_message, subscribe_to_topic, unsubscribe_from_topic, delete_one_topic
)
from controllers.queue_controller import subscribe_to_queue, send_message, receive_message, delete_one_queue, unsubscribe_to_queue
from fastapi import HTTPException, BackgroundTasks


class MOMService(mom_pb2_grpc.TopicServiceServicer):

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
                    "owner": request.owner
                })
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
                # Actualizar mensajes del tópico
                topic['messages'].append(request.message)
                
                # Actualizar pending_messages para cada suscriptor
                for subscriber in request.subscribers:
                    if subscriber in topic['pending_messages']:
                        topic['pending_messages'][subscriber].append(request.message)
                    else:
                        topic['pending_messages'][subscriber] = [request.message]
                
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


def serve():
    print("GRPC RUNNING...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    mom_pb2_grpc.add_TopicServiceServicer_to_server(MOMService(), server)
    mom_pb2_grpc.add_QueueServiceServicer_to_server(
        QueueServiceHandler(), server)
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
