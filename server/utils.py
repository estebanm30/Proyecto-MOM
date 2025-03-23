from fastapi import HTTPException
from state import active_sessions
from zookeeper import get_tokens


def verify_token(token: str):
    tokens = get_tokens()
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
