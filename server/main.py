import uvicorn
import sys
from fastapi import FastAPI
from routes import router
import atexit
from zookeeper import close_connection
import grpc_server
from concurrent import futures
import mom_pb2_grpc


app = FastAPI()

app.include_router(router)
atexit.register(close_connection)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
    server = grpc_server.server(futures.ThreadPoolExecutor(max_workers=10))
    mom_pb2_grpc.add_MOMServiceServicer_to_server(grpc_server.MOMService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
