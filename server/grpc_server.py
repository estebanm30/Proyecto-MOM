import grpc
from concurrent import futures
import time
import mom_pb2
import mom_pb2_grpc

from controllers.topic_controller import (
    publish_message, subscribe_to_topic, unsubscribe_from_topic, delete_one_topic
)
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


def serve():
    print("GRPC RUNNING...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    mom_pb2_grpc.add_TopicServiceServicer_to_server(MOMService(), server)
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
