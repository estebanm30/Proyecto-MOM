from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import insert_queue, find_queue, find_all_queues, update_queue, delete_queue

app = FastAPI()


class QueueModel(BaseModel):
    name: str


@app.post("/queue/create/")
def create_queue(queue: QueueModel):
    if find_queue(queue.name):
        raise HTTPException(status_code=400, detail="Queue already exists")
    insert_queue({"name": queue.name, "messages": []})
    print(list(find_all_queues()))
    return {"message": "Queue created"}


@app.post("/queue/send/")
def send_message(queueName: str, message: str):
    queue = find_queue(queueName)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    queue["messages"].append(message)
    update_queue(queueName, queue["messages"])

    print(find_queue(queueName)["messages"])
    return {"message": "Message sent"}


@app.get("/queue/receive/")
def receive_message(queueName: str):
    queue = find_queue(queueName)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    if len(queue["messages"]) == 0:
        raise HTTPException(status_code=404, detail="Queue is empty")

    msg = queue["messages"].pop(0)
    update_queue(queueName, queue["messages"])

    return {"message": msg}

@app.delete("/queue/")
def delete_one_queue(queueName: str):
    queue = find_queue(queueName)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")

    delete_queue(queueName)
    return {"message": "Queue deleted"}
    
