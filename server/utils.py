from fastapi import HTTPException
from state import active_sessions


def verify_token(token: str):
    if token not in active_sessions:
        raise HTTPException(status_code=401, detail="Invalid token")