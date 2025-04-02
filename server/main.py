import uvicorn
import sys
from fastapi import FastAPI
from routes import router
import atexit
from zookeeper import close_connection
import grpc_server


app = FastAPI()

app.include_router(router)
atexit.register(close_connection)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    grpc_server.start_grpc_server()
    uvicorn.run(app, host="0.0.0.0", port=port)
