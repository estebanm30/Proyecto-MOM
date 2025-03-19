from fastapi import APIRouter, BackgroundTasks
from controllers.auth_controller import connect_client
from controllers.queue_controller import create_queue, send_message, receive_message, delete_one_queue
from controllers.topic_controller import create_topic, subscribe_to_topic, unsubscribe_from_topic, publish_message, get_messages
from models import AuthModel, QueueModel, TopicModel

router = APIRouter()

#AUTH ROUTES

@router.post("/connect/")
def connect(auth: AuthModel):
    return connect_client(auth)

#QUEUE ROUTES

@router.post("/queue/create/")
def createq(queue: QueueModel, token: str):
    return create_queue(queue,token)

@router.post("/queue/send/")
def sendq(queue_name: str, message: str, token: str):
    return send_message(queue_name,message,token)

@router.get("/queue/receive/")
def receiveq(queue_name: str, token: str):
    return receive_message(queue_name,token)

@router.delete("/queue/")
def deleteq(queue_name: str, token: str):
    return delete_one_queue(queue_name,token)

#TOPICS CONTROLLERS
@router.post("/topic/create/")
def createt(topic: TopicModel, token: str):
    return create_topic(topic,token)

@router.put("/topic/subscribe/")
def suscribet(topic_name: str, token: str):
    return subscribe_to_topic(topic_name,token)

@router.put("/topic/unsubscribe/")
def unsiscribet(topic_name: str, token: str):
    return unsubscribe_from_topic(topic_name,token)

@router.post("/topic/publish/")
def publisht(topic_name: str, message: str, token: str, background_tasks: BackgroundTasks):
    return publish_message(topic_name,message,token,background_tasks)

@router.get("/topic/messages/")
def get_messagest(token: str):
    return get_messages(token)