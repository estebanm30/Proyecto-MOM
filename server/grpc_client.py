import grpc
import mom_pb2
import mom_pb2_grpc

# Dirección del otro servidor MOM
SERVER_ADDRESS = "localhost:50051"

def update_queue(queue_name, messages):

    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = mom_pb2_grpc.MOMServiceStub(channel)
        request = mom_pb2.UpdateQueueRequest(queue_name=queue_name, messages=messages)
        response = stub.UpdateQueue(request)
        print(f"✅ Respuesta del servidor: {response.success}")

def update_topic(topic_name, messages):

    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = mom_pb2_grpc.MOMServiceStub(channel)
        request = mom_pb2.UpdateTopicRequest(topic_name=topic_name, messages=messages)
        response = stub.UpdateTopic(request)
        print(f"✅ Respuesta del servidor: {response.success}")

# Ejemplo de uso
if __name__ == "__main__":
    update_queue("mi_cola", ["Mensaje 1", "Mensaje 2"])
    update_topic("mi_tópico", ["Mensaje A", "Mensaje B"])