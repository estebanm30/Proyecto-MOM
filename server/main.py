from fastapi import FastAPI, HTTPException
from database import insert_queue, find_queue, find_all_queues, update_queue, delete_queue
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
    if find_queue(queue.name):
        raise HTTPException(status_code=400, detail="Queue already exists")
    insert_queue({"name": queue.name, "messages": []})
    print(list(find_all_queues()))
    return {"message": "Queue created"}


@app.post("/queue/send/")
def send_message(queueName: str, message: str, token: str):
    verify_token(token)
    queue = find_queue(queueName)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    queue["messages"].append(message)
    update_queue(queueName, queue["messages"])

    print(find_queue(queueName)["messages"])
    return {"message": "Message sent"}


@app.get("/queue/receive/")
def receive_message(queueName: str, token: str):
    verify_token(token)
    queue = find_queue(queueName)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    if len(queue["messages"]) == 0:
        raise HTTPException(status_code=404, detail="Queue is empty")
    msg = queue["messages"].pop(0)
    update_queue(queueName, queue["messages"])
    return {"message": msg}


@app.delete("/queue/")
def delete_one_queue(queueName: str, token: str):
    verify_token(token)
    queue = find_queue(queueName)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    delete_queue(queueName)
    return {"message": "Queue deleted"}
