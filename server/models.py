from pydantic import BaseModel

class QueueModel(BaseModel):
    name: str

class TopicModel(BaseModel):
    name: str

class AuthModel(BaseModel):
    user: str
    password: str