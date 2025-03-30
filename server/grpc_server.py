import grpc
from concurrent import futures
import time
import mom_pb2
import mom_pb2_grpc

class MOMService(mom_pb2_grpc.MOMServiceServicer):
    def UpdateQueue(self, request, context):

        print(f"🔄 Updating Queues: {request.queue_name}")
        print(f"Updated Messages: {request.messages}")
        return mom_pb2.UpdateQueueResponse(success=True)

    def UpdateTopic(self, request, context):

        print(f"🔄 Updating Topic: {request.topic_name}")
        print(f"Topic Changes: {request.messages}")
        return mom_pb2.UpdateTopicResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    mom_pb2_grpc.add_MOMServiceServicer_to_server(MOMService(), server)
    
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

if __name__ == "__main__":
    serve()