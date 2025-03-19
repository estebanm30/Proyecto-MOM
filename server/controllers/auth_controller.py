import secrets
from fastapi import HTTPException
from database import find_client
from models import AuthModel
from state import active_sessions

def connect_client(auth: AuthModel):
    print("connecting user")
    client = find_client(auth.user)
    if not client:
        print("USER NOT FOUND")
        raise HTTPException(status_code=401, detail="Client no allowed")
    else:
        print("USER FINDED")
        if auth.password == client["password"]:
            token = secrets.token_hex(16)
            active_sessions[token] = auth.user
            return {"message": "Connected to server", "token": token}
    