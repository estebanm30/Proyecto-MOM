from fastapi import FastAPI, HTTPException, BackgroundTasks
from database import insert_queue, find_queue, find_all_queues, update_queue, delete_queue, insert_topic, find_all_topics, find_topic, update_topic, delete_topic
from models import QueueModel, TopicModel, AuthModel
from collections import deque
import secrets

app = FastAPI()
queues = {}
users = {}
active_sessions = {}
subscriptions = {}
pending_messages = {}

with open("users.txt", "r", encoding="utf-8") as file:
    for line in file:
        user, password = line.strip().split(",")
        users[user] = password


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


@app.post("/topic/create/")
def create_topic(topic: TopicModel, token: str):
    verify_token(token)
    if find_topic(topic.name):
        raise HTTPException(status_code=400, detail="Topic already exists")
    insert_topic({"name": topic.name, "subscribers": [],
                 "messages": [], "pending_messages": {}})
    return {"message": "Topic created"}


@app.put("/topic/subscribe/")
def subscribe_to_topic(topic_name: str, token: str):
    print("Existing topics:", queues.keys())
    verify_token(token)
    user = active_sessions[token]
    topic = find_topic(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if user in topic['subscribers']:
        raise HTTPException(status_code=400, detail="Already subscribed")
    else:
        topic['subscribers'].append(user)
        topic['pending_messages'][user] = []

    update_topic(topic_name, topic)
    return {"message": f"{user} subscribed to {topic_name}"}


@app.put("/topic/unsubscribe/")
def unsubscribe_from_topic(topic_name: str, token: str):
    verify_token(token)
    user = active_sessions[token]
    topic = find_topic(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if user not in topic['subscribers']:
        raise HTTPException(status_code=400, detail="Not subscribed")
    else:
        topic['subscribers'].remove(user)
        topic['pending_messages'].pop(user, None)
    update_topic(topic_name, topic)

    topics = find_all_topics()
    for topic in topics:
        cont = 0
        for pending_message in topic['pending_messages'].values():
            if len(pending_message) > 0:
                cont += 1
        if cont == 0:
            topic['messages'] = []
            update_topic(topic['name'], topic)
    return {"message": f"{user} unsubscribed from {topic_name}"}


@app.post("/topic/publish/")
def publish_message(topic_name: str, message: str, token: str, background_tasks: BackgroundTasks):
    verify_token(token)
    topic = find_topic(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic['messages'].append(message)
    for subscriber in topic['subscribers']:
        topic['pending_messages'][subscriber].append(message)
    update_topic(topic_name, topic)

    return {"message": f"Message published to {len(topic['subscribers'])} subscribers"}


@app.get("/topic/messages/")
def get_messages(token: str):
    verify_token(token)
    user = active_sessions[token]
    topics = find_all_topics()
    messages = []
    for topic in topics:
        if user in topic['subscribers'] and topic['pending_messages'][user]:
            messages.append(
                {"topic": topic['name'], "message": topic['pending_messages'][user]})
            topic['pending_messages'][user] = []
            update_topic(topic['name'], topic)
    topics = find_all_topics()
    for topic in topics:
        cont = 0
        for pending_message in topic['pending_messages'].values():
            if len(pending_message) > 0:
                cont += 1
        if cont == 0:
            topic['messages'] = []
            update_topic(topic['name'], topic)

    return {"messages": messages}
