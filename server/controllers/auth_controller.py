import secrets
from fastapi import HTTPException
from database import find_client
from models import AuthModel
from zookeeper import zk

def connect_client(auth: AuthModel):
    print("connecting user")
    client = find_client(auth.user)
    if not client:
        print("USER NOT FOUND")
        raise HTTPException(status_code=401, detail="Client not allowed")
    else:
        print("USER FOUND")
        if auth.password == client["password"]:
            token = secrets.token_hex(16)
            path = f"/tokens/{token}"

            if not zk.exists(path):
                zk.create(path, auth.user.encode(), makepath=True)
            else:
                zk.set(path, auth.user.encode())

            return {"message": "Connected to server", "token": token}
        else:
            raise HTTPException(status_code=401, detail="Wrong password")
