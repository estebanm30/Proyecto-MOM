from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from collections import deque
import secrets

app = FastAPI()
queues = {}
users = {}
active_sessions = {}

with open("users.txt", "r", encoding="utf-8") as file:
    for line in file:
        user, password = line.strip().split(",")
        users[user] = password

class QueueModel(BaseModel):
    name: str

class AuthModel(BaseModel):
    user: str
    password: str

@app.post("/connect/")
def connect_client(auth: AuthModel):
    if auth.user in users and auth.password == users[auth.user]:
        token = secrets.token_hex(16)
        active_sessions[token] = auth.user
        return {"message": "Connected to server", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


def verify_token(token: str):
    if token not in active_sessions:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/queue/create/")
def create_queue(queue: QueueModel, token: str):
    verify_token(token)
    if queue.name in queues:
        raise HTTPException(status_code=400, detail="Queue already exists")
    queues[queue.name] = deque()
    print(queues)
    return {"message": "Queue created"}


@app.post("/queue/send/")
def send_message(queue: str, message: str, token: str):
    verify_token(token)
    if not queue in queues:
        raise HTTPException(status_code=404, detail="Queue not found")
    queues[queue].append(message)
    print(queues)
    return {"message": "Message sent"}


@app.get("/queue/receive/")
def receive_message(queue: str, token: str):
    verify_token(token)
    if not queue in queues:
        raise HTTPException(status_code=404, detail="Queue not found")
    if len(queues[queue]) == 0:
        raise HTTPException(status_code=404, detail="Queue is empty")
    msg = queues[queue].pop()
    print(queues)
    return {"message": msg}