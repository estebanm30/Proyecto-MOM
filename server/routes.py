from fastapi import APIRouter, BackgroundTasks
from controllers.auth_controller import connect_client
from controllers.queue_controller import create_queue, send_message, receive_message, delete_one_queue, get_queues, subscribe_to_queue, get_messages_queue
from controllers.topic_controller import create_topic, subscribe_to_topic, unsubscribe_from_topic, publish_message, get_messages, delete_one_topic, get_topics
from models import AuthModel, QueueModel, TopicModel

router = APIRouter()

# AUTH ROUTES

@router.post("/connect/")
def connect(auth: AuthModel):
    return connect_client(auth)

# QUEUE ROUTES

@router.get("/queue/")
def receiveq(token: str):
    return get_queues(token)


@router.post("/queue/create/")
def createq(queue: QueueModel, token: str):
    return create_queue(queue, token)


@router.put("/queue/subscribe/")
def subscribet(queue_name: str, token: str):
    return subscribe_to_queue(queue_name, token)


@router.post("/queue/send/")
def sendq(queue_name: str, message: str, token: str, background_tasks: BackgroundTasks):
    return send_message(queue_name, message, token, background_tasks)


@router.get("/queue/receive/")
def receiveq(queue_name: str, token: str):
    return receive_message(queue_name, token)

@router.get("/queue/messages/")
def get_messagest(token: str):
    return get_messages_queue(token)
    
@router.delete("/queue/")
def deleteq(queue_name: str, token: str):
    return delete_one_queue(queue_name, token)


# TOPICS ROUTERS


@router.get("/topic/")
def receivet(token: str):
    return get_topics(token)


@router.post("/topic/create/")
def createt(topic: TopicModel, token: str):
    return create_topic(topic, token)


@router.put("/topic/subscribe/")
def suscribet(topic_name: str, token: str):
    return subscribe_to_topic(topic_name, token)


@router.put("/topic/unsubscribe/")
def unsiscribet(topic_name: str, token: str):
    return unsubscribe_from_topic(topic_name, token)


@router.post("/topic/publish/")
def publisht(topic_name: str, message: str, token: str, background_tasks: BackgroundTasks):
    return publish_message(topic_name, message, token, background_tasks)


@router.get("/topic/messages/")
def get_messagest(token: str):
    return get_messages(token)


@router.delete("/topic/")
def deletet(topic_name: str, token: str):
    return delete_one_topic(topic_name, token)
