from fastapi import HTTPException
from database import insert_queue, find_queue, find_all_queues, update_queue, delete_queue
from models import QueueModel
from utils import verify_token
from state import active_sessions


def get_queues(token: str):
    verify_token(token)
    queues = find_all_queues()
    names = []
    for queue in queues:
        names.append(queue["name"])
    return names


def create_queue(queue: QueueModel, token: str):
    verify_token(token)
    client = active_sessions[token]
    if find_queue(queue.name):
        raise HTTPException(status_code=400, detail="Queue already exists")
    insert_queue({"name": queue.name, "messages": [], "owner": client})
    print(list(find_all_queues()))
    return {"message": "Queue created"}


def send_message(queue_name: str, message: str, token: str):
    verify_token(token)
    queue = find_queue(queue_name)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    queue["messages"].append(message)
    update_queue(queue_name, queue["messages"])

    print(find_queue(queue_name)["messages"])
    return {"message": "Message sent"}


def receive_message(queue_name: str, token: str):
    verify_token(token)
    queue = find_queue(queue_name)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    if len(queue["messages"]) == 0:
        raise HTTPException(status_code=404, detail="Queue is empty")
    msg = queue["messages"].pop(0)
    update_queue(queue_name, queue["messages"])
    return {"message": msg}


def delete_one_queue(queue_name: str, token: str):
    verify_token(token)
    client = active_sessions[token]
    queue = find_queue(queue_name)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")
    if queue["owner"] == client:
        delete_queue(queue_name)
    else:
        return {"message": "You cannot delete this queue"}
    return {"message": "Queue deleted"}
