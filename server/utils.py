from fastapi import HTTPException
from state import active_sessions
from zookeeper import get_tokens
from zookeeper import get_topic_server
from database import find_topic


def verify_token(token: str):
    tokens = get_tokens()
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_redirect(topic_name: str):
    if find_topic(topic_name) is None:
        responsible_server = get_topic_server(topic_name)

        if responsible_server:
            return {
                "redirect_to": responsible_server,
            }
        raise HTTPException(status_code=404, detail="Topic not found.")
    return None