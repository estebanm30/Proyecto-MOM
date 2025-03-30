import grpc
from concurrent import futures
import time
import mom_pb2
import mom_pb2_grpc

class MOMService(mom_pb2_grpc.MOMServiceServicer):
    def UpdateQueue(self, request, context):

        print(f"🔄 Actualizando cola: {request.queue_name}")
        print(f"Mensajes recibidos: {request.messages}")
        return mom_pb2.UpdateQueueResponse(success=True)

    def UpdateTopic(self, request, context):

        print(f"🔄 Actualizando tópico: {request.topic_name}")
        print(f"Mensajes recibidos: {request.messages}")
        return mom_pb2.UpdateTopicResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mom_pb2_grpc.add_MOMServiceServicer_to_server(MOMService(), server)
    
    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"🚀 Servidor gRPC corriendo en el puerto {port}")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("🛑 Cerrando servidor gRPC")
        server.stop(0)

if __name__ == "__main__":
    serve()