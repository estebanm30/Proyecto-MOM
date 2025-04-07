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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tmom.proto\"8\n\x13SubscriptionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"D\n\x0ePublishRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\"2\n\rDeleteRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t\"1\n\x0cQueueRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"D\n\x0eMessageRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\"\"\n\x0fMessageResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1d\n\x0cTokenRequest\x12\r\n\x05token\x18\x01 \x01(\t\"(\n\x11QueueListResponse\x12\x13\n\x0bqueue_names\x18\x01 \x03(\t\"=\n\x18QueueSubscriptionRequest\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\":\n\x15ReplicateTopicRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t\"F\n\x1cReplicateSubscriptionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x12\n\nsubscriber\x18\x02 \x01(\t\"S\n\x17ReplicateMessageRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x13\n\x0bsubscribers\x18\x03 \x03(\t\"H\n\x1eReplicateUnsubscriptionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x12\n\nsubscriber\x18\x02 \x01(\t\"m\n\x1dReplicateTopicDeletionRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\r\n\x05owner\x18\x02 \x01(\t\x12\x14\n\x0clast_message\x18\x03 \x01(\t\x12\x13\n\x0bsubscribers\x18\x04 \x03(\t2\xfa\x03\n\x0cTopicService\x12,\n\tSubscribe\x12\x14.SubscriptionRequest\x1a\t.Response\x12.\n\x0bUnsubscribe\x12\x14.SubscriptionRequest\x1a\t.Response\x12%\n\x07Publish\x12\x0f.PublishRequest\x1a\t.Response\x12(\n\x0b\x44\x65leteTopic\x12\x0e.DeleteRequest\x1a\t.Response\x12\x33\n\x0eReplicateTopic\x12\x16.ReplicateTopicRequest\x1a\t.Response\x12\x41\n\x15ReplicateSubscription\x12\x1d.ReplicateSubscriptionRequest\x1a\t.Response\x12\x37\n\x10ReplicateMessage\x12\x18.ReplicateMessageRequest\x1a\t.Response\x12\x45\n\x17ReplicateUnsubscription\x12\x1f.ReplicateUnsubscriptionRequest\x1a\t.Response\x12\x43\n\x16ReplicateTopicDeletion\x12\x1e.ReplicateTopicDeletionRequest\x1a\t.Response2\xe0\x02\n\x0cQueueService\x12\'\n\x0b\x43reateQueue\x12\r.QueueRequest\x1a\t.Response\x12\x36\n\x0eSubscribeQueue\x12\x19.QueueSubscriptionRequest\x1a\t.Response\x12)\n\x0bSendMessage\x12\x0f.MessageRequest\x1a\t.Response\x12\x31\n\x0eReceiveMessage\x12\r.QueueRequest\x1a\x10.MessageResponse\x12\'\n\x0b\x44\x65leteQueue\x12\r.QueueRequest\x1a\t.Response\x12.\n\tGetQueues\x12\r.TokenRequest\x1a\x12.QueueListResponse\x12\x38\n\x10UnsubscribeQueue\x12\x19.QueueSubscriptionRequest\x1a\t.Responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mom_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SUBSCRIPTIONREQUEST']._serialized_start=13
  _globals['_SUBSCRIPTIONREQUEST']._serialized_end=69
  _globals['_PUBLISHREQUEST']._serialized_start=71
  _globals['_PUBLISHREQUEST']._serialized_end=139
  _globals['_DELETEREQUEST']._serialized_start=141
  _globals['_DELETEREQUEST']._serialized_end=191
  _globals['_RESPONSE']._serialized_start=193
  _globals['_RESPONSE']._serialized_end=220
  _globals['_QUEUEREQUEST']._serialized_start=222
  _globals['_QUEUEREQUEST']._serialized_end=271
  _globals['_MESSAGEREQUEST']._serialized_start=273
  _globals['_MESSAGEREQUEST']._serialized_end=341
  _globals['_MESSAGERESPONSE']._serialized_start=343
  _globals['_MESSAGERESPONSE']._serialized_end=377
  _globals['_TOKENREQUEST']._serialized_start=379
  _globals['_TOKENREQUEST']._serialized_end=408
  _globals['_QUEUELISTRESPONSE']._serialized_start=410
  _globals['_QUEUELISTRESPONSE']._serialized_end=450
  _globals['_QUEUESUBSCRIPTIONREQUEST']._serialized_start=452
  _globals['_QUEUESUBSCRIPTIONREQUEST']._serialized_end=513
  _globals['_REPLICATETOPICREQUEST']._serialized_start=515
  _globals['_REPLICATETOPICREQUEST']._serialized_end=573
  _globals['_REPLICATESUBSCRIPTIONREQUEST']._serialized_start=575
  _globals['_REPLICATESUBSCRIPTIONREQUEST']._serialized_end=645
  _globals['_REPLICATEMESSAGEREQUEST']._serialized_start=647
  _globals['_REPLICATEMESSAGEREQUEST']._serialized_end=730
  _globals['_REPLICATEUNSUBSCRIPTIONREQUEST']._serialized_start=732
  _globals['_REPLICATEUNSUBSCRIPTIONREQUEST']._serialized_end=804
  _globals['_REPLICATETOPICDELETIONREQUEST']._serialized_start=806
  _globals['_REPLICATETOPICDELETIONREQUEST']._serialized_end=915
  _globals['_TOPICSERVICE']._serialized_start=918
  _globals['_TOPICSERVICE']._serialized_end=1424
  _globals['_QUEUESERVICE']._serialized_start=1427
  _globals['_QUEUESERVICE']._serialized_end=1779
# @@protoc_insertion_point(module_scope)
