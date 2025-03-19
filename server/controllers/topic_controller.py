import time
from fastapi import HTTPException, BackgroundTasks
from database import insert_topic, find_all_topics, find_topic, update_topic, delete_topic
from models import TopicModel
from utils import verify_token
from state import active_sessions


def get_topics(token: str):
    verify_token(token)
    topics = find_all_topics()
    names = []
    for topic in topics:
        names.append(topic["name"])
    return names

def create_topic(topic: TopicModel, token: str):
    verify_token(token)
    client = active_sessions[token]
    if find_topic(topic.name):
        raise HTTPException(status_code=400, detail="Topic already exists")
    insert_topic({"name": topic.name, "subscribers": [],
                 "messages": [], "pending_messages": {}, "owner":client})
    return {"message": "Topic created"}


def subscribe_to_topic(topic_name: str, token: str):
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

def delete_one_topic(topic_name: str, token: str):
    verify_token(token)
    client = active_sessions[token]
    topic = find_topic(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if topic["owner"] == client:

        message = f"The topic {topic_name} has been eliminated by the owner"
        topic['messages'].append(message)
        for subscriber in topic['subscribers']:
            topic['pending_messages'][subscriber].append(message)
        update_topic(topic_name, topic)
        time.sleep(2)
        delete_topic(topic_name)
    else:
        return {"message": "You cannot delete this topic"}
    return {"message": "Topic deleted"}


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