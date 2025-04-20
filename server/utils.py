from fastapi import HTTPException
from zk_utils import get_tokens
from zk_utils import get_topic_server
from database import find_topic
from database import find_queue
from zk_utils import get_queue_server

def verify_token(token: str):
    tokens = get_tokens()
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_redirect(topic_name: str):
    if find_topic(topic_name) is None:
        responsible_server = get_topic_server(topic_name)
        if responsible_server:
            return responsible_server
        raise HTTPException(status_code=404, detail="Topic not found.")
    return None

def check_redirect_queues(queue_name: str):
    if find_queue(queue_name) is None:
        responsible_server = get_queue_server(queue_name)
        if responsible_server:
            return responsible_server
        raise HTTPException(status_code=404, detail="Queue not found.")
    return None