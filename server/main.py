import uvicorn
import sys
from fastapi import FastAPI
from routes import router
import atexit
from zookeeper import close_connection


app = FastAPI()

app.include_router(router)
atexit.register(close_connection)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000  # Usa el puerto proporcionado o 8000 por defecto
    uvicorn.run(app, host="0.0.0.0", port=port)