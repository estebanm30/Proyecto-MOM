import secrets
from fastapi import HTTPException
from models import AuthModel
from state import users,active_sessions

def connect_client(auth: AuthModel):
    with open("users.txt", "r", encoding="utf-8") as file:
        for line in file:
            user, password = line.strip().split(",")
            users[user] = password
    if auth.user in users and auth.password == users[auth.user]:
        token = secrets.token_hex(16)
        active_sessions[token] = auth.user
        return {"message": "Connected to server", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")