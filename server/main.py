from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from collections import deque

app = FastAPI()
queues = {}

class QueueModel(BaseModel):
    name: str

@app.post("/queue/create/")
def create_queue(queue: QueueModel):
    if queue.name in queues:
        raise HTTPException(status_code=400, detail="Queue already exists")
    queues[queue.name] = deque()
    print(queues)
    return {"message": "Queue created"}


@app.post("/queue/send/")
def send_message(queue: str, message: str):
    if not queue in queues:
        raise HTTPException(status_code=404, detail="Queue not found")
    queues[queue].append(message)
    print(queues)
    return {"message": "Message sent"}


@app.get("/queue/receive/")
def receive_message(queue: str):
    if not queue in queues:
        raise HTTPException(status_code=404, detail="Queue not found")
    if len(queues[queue]) == 0:
        raise HTTPException(status_code=404, detail="Queue is empty")
    msg = queues[queue].pop()
    print(queues)
    return {"message": msg}
