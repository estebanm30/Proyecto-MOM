# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mom.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'mom.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tmom.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xf9\x01\n\x05Topic\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bsubscribers\x18\x02 \x03(\t\x12\x10\n\x08messages\x18\x03 \x03(\t\x12\x35\n\x10pending_messages\x18\x04 \x03(\x0b\x32\x1b.Topic.PendingMessagesEntry\x12\r\n\x05owner\x18\x05 \x01(\t\x12/\n\x0bupdate_date\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\x44\n\x14PendingMessagesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1b\n\x05value\x18\x02 \x01(\x0b\x32\x0c.MessageList:\x02\x38\x01\"\xf9\x01\n\x05Queue\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bsubscribers\x18\x02 \x03(\t\x12\x10\n\x08messages\x18\x03 \x03(\t\x12\x35\n\x10pending_messages\x18\x04 \x03(\x0b\x32\x1b.Queue.PendingMessagesEntry\x12\r\n\x05owner\x18\x05 \x01(\t\x12/\n\x0bupdate_date\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\x44\n\x14PendingMessagesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1b\n\x05value\x18\x02 \x01(\x0b\x32\x0c.MessageList:\x02\x38\x01\"\x1f\n\x0bMessageList\x12\x10\n\x08messages\x18\x01 \x03(\t\"8\n\x13SubscriptionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"D\n\x0ePublishRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\"2\n\rDeleteRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t\"1\n\x0cQueueRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"D\n\x0eMessageRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\"\"\n\x0fMessageResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1d\n\x0cTokenRequest\x12\r\n\x05token\x18\x01 \x01(\t\"(\n\x11QueueListResponse\x12\x13\n\x0bqueue_names\x18\x01 \x03(\t\"=\n\x18QueueSubscriptionRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\":\n\x15ReplicateTopicRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t\"F\n\x1cReplicateSubscriptionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x12\n\nsubscriber\x18\x02 \x01(\t\"S\n\x17ReplicateMessageRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x13\n\x0bsubscribers\x18\x03 \x03(\t\"H\n\x1eReplicateUnsubscriptionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x12\n\nsubscriber\x18\x02 \x01(\t\"m\n\x1dReplicateTopicDeletionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t\x12\x14\n\x0clast_message\x18\x03 \x01(\t\x12\x13\n\x0bsubscribers\x18\x04 \x03(\t\":\n\x15ReplicateQueueRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t\"K\n!ReplicateQueueSubscriptionRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\x12\n\nsubscriber\x18\x02 \x01(\t\"w\n\x1cReplicateQueueMessageRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x12\n\nsubscriber\x18\x03 \x01(\t\x12\x1e\n\x16\x63urrent_subscriber_idx\x18\x04 \x01(\x05\"M\n#ReplicateQueueUnsubscriptionRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\x12\n\nsubscriber\x18\x02 \x01(\t\"W\n\x1dReplicateQueueDeletionRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t\x12\x13\n\x0bsubscribers\x18\x03 \x03(\t\"Z\n\x1fReplicateMessageDeletionRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\x12\n\nsubscriber\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t2\xfa\x03\n\x0cTopicService\x12,\n\tSubscribe\x12\x14.SubscriptionRequest\x1a\t.Response\x12.\n\x0bUnsubscribe\x12\x14.SubscriptionRequest\x1a\t.Response\x12%\n\x07Publish\x12\x0f.PublishRequest\x1a\t.Response\x12(\n\x0b\x44\x65leteTopic\x12\x0e.DeleteRequest\x1a\t.Response\x12\x33\n\x0eReplicateTopic\x12\x16.ReplicateTopicRequest\x1a\t.Response\x12\x41\n\x15ReplicateSubscription\x12\x1d.ReplicateSubscriptionRequest\x1a\t.Response\x12\x37\n\x10ReplicateMessage\x12\x18.ReplicateMessageRequest\x1a\t.Response\x12\x45\n\x17ReplicateUnsubscription\x12\x1f.ReplicateUnsubscriptionRequest\x1a\t.Response\x12\x43\n\x16ReplicateTopicDeletion\x12\x1e.ReplicateTopicDeletionRequest\x1a\t.Response2\x84\x06\n\x0cQueueService\x12\'\n\x0b\x43reateQueue\x12\r.QueueRequest\x1a\t.Response\x12\x36\n\x0eSubscribeQueue\x12\x19.QueueSubscriptionRequest\x1a\t.Response\x12)\n\x0bSendMessage\x12\x0f.MessageRequest\x1a\t.Response\x12\x31\n\x0eReceiveMessage\x12\r.QueueRequest\x1a\x10.MessageResponse\x12\'\n\x0b\x44\x65leteQueue\x12\r.QueueRequest\x1a\t.Response\x12.\n\tGetQueues\x12\r.TokenRequest\x1a\x12.QueueListResponse\x12\x38\n\x10UnsubscribeQueue\x12\x19.QueueSubscriptionRequest\x1a\t.Response\x12\x33\n\x0eReplicateQueue\x12\x16.ReplicateQueueRequest\x1a\t.Response\x12K\n\x1aReplicateQueueSubscription\x12\".ReplicateQueueSubscriptionRequest\x1a\t.Response\x12\x41\n\x15ReplicateQueueMessage\x12\x1d.ReplicateQueueMessageRequest\x1a\t.Response\x12O\n\x1cReplicateQueueUnsubscription\x12$.ReplicateQueueUnsubscriptionRequest\x1a\t.Response\x12\x43\n\x16ReplicateQueueDeletion\x12\x1e.ReplicateQueueDeletionRequest\x1a\t.Response\x12G\n\x18ReplicateMessageDeletion\x12 .ReplicateMessageDeletionRequest\x1a\t.Response2j\n\tOnBooting\x12-\n\x0bupdateTopic\x12\x16.ReplicateTopicRequest\x1a\x06.Topic\x12.\n\x0cupdateQueues\x12\x16.ReplicateQueueRequest\x1a\x06.Queueb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mom_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TOPIC_PENDINGMESSAGESENTRY']._loaded_options = None
  _globals['_TOPIC_PENDINGMESSAGESENTRY']._serialized_options = b'8\001'
  _globals['_QUEUE_PENDINGMESSAGESENTRY']._loaded_options = None
  _globals['_QUEUE_PENDINGMESSAGESENTRY']._serialized_options = b'8\001'
  _globals['_TOPIC']._serialized_start=47
  _globals['_TOPIC']._serialized_end=296
  _globals['_TOPIC_PENDINGMESSAGESENTRY']._serialized_start=228
  _globals['_TOPIC_PENDINGMESSAGESENTRY']._serialized_end=296
  _globals['_QUEUE']._serialized_start=299
  _globals['_QUEUE']._serialized_end=548
  _globals['_QUEUE_PENDINGMESSAGESENTRY']._serialized_start=228
  _globals['_QUEUE_PENDINGMESSAGESENTRY']._serialized_end=296
  _globals['_MESSAGELIST']._serialized_start=550
  _globals['_MESSAGELIST']._serialized_end=581
  _globals['_SUBSCRIPTIONREQUEST']._serialized_start=583
  _globals['_SUBSCRIPTIONREQUEST']._serialized_end=639
  _globals['_PUBLISHREQUEST']._serialized_start=641
  _globals['_PUBLISHREQUEST']._serialized_end=709
  _globals['_DELETEREQUEST']._serialized_start=711
  _globals['_DELETEREQUEST']._serialized_end=761
  _globals['_RESPONSE']._serialized_start=763
  _globals['_RESPONSE']._serialized_end=790
  _globals['_QUEUEREQUEST']._serialized_start=792
  _globals['_QUEUEREQUEST']._serialized_end=841
  _globals['_MESSAGEREQUEST']._serialized_start=843
  _globals['_MESSAGEREQUEST']._serialized_end=911
  _globals['_MESSAGERESPONSE']._serialized_start=913
  _globals['_MESSAGERESPONSE']._serialized_end=947
  _globals['_TOKENREQUEST']._serialized_start=949
  _globals['_TOKENREQUEST']._serialized_end=978
  _globals['_QUEUELISTRESPONSE']._serialized_start=980
  _globals['_QUEUELISTRESPONSE']._serialized_end=1020
  _globals['_QUEUESUBSCRIPTIONREQUEST']._serialized_start=1022
  _globals['_QUEUESUBSCRIPTIONREQUEST']._serialized_end=1083
  _globals['_REPLICATETOPICREQUEST']._serialized_start=1085
  _globals['_REPLICATETOPICREQUEST']._serialized_end=1143
  _globals['_REPLICATESUBSCRIPTIONREQUEST']._serialized_start=1145
  _globals['_REPLICATESUBSCRIPTIONREQUEST']._serialized_end=1215
  _globals['_REPLICATEMESSAGEREQUEST']._serialized_start=1217
  _globals['_REPLICATEMESSAGEREQUEST']._serialized_end=1300
  _globals['_REPLICATEUNSUBSCRIPTIONREQUEST']._serialized_start=1302
  _globals['_REPLICATEUNSUBSCRIPTIONREQUEST']._serialized_end=1374
  _globals['_REPLICATETOPICDELETIONREQUEST']._serialized_start=1376
  _globals['_REPLICATETOPICDELETIONREQUEST']._serialized_end=1485
  _globals['_REPLICATEQUEUEREQUEST']._serialized_start=1487
  _globals['_REPLICATEQUEUEREQUEST']._serialized_end=1545
  _globals['_REPLICATEQUEUESUBSCRIPTIONREQUEST']._serialized_start=1547
  _globals['_REPLICATEQUEUESUBSCRIPTIONREQUEST']._serialized_end=1622
  _globals['_REPLICATEQUEUEMESSAGEREQUEST']._serialized_start=1624
  _globals['_REPLICATEQUEUEMESSAGEREQUEST']._serialized_end=1743
  _globals['_REPLICATEQUEUEUNSUBSCRIPTIONREQUEST']._serialized_start=1745
  _globals['_REPLICATEQUEUEUNSUBSCRIPTIONREQUEST']._serialized_end=1822
  _globals['_REPLICATEQUEUEDELETIONREQUEST']._serialized_start=1824
  _globals['_REPLICATEQUEUEDELETIONREQUEST']._serialized_end=1911
  _globals['_REPLICATEMESSAGEDELETIONREQUEST']._serialized_start=1913
  _globals['_REPLICATEMESSAGEDELETIONREQUEST']._serialized_end=2003
  _globals['_TOPICSERVICE']._serialized_start=2006
  _globals['_TOPICSERVICE']._serialized_end=2512
  _globals['_QUEUESERVICE']._serialized_start=2515
  _globals['_QUEUESERVICE']._serialized_end=3287
  _globals['_ONBOOTING']._serialized_start=3289
  _globals['_ONBOOTING']._serialized_end=3395
# @@protoc_insertion_point(module_scope)
