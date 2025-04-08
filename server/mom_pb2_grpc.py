# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import mom_pb2 as mom__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in mom_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TopicServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Subscribe = channel.unary_unary(
                '/TopicService/Subscribe',
                request_serializer=mom__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.Unsubscribe = channel.unary_unary(
                '/TopicService/Unsubscribe',
                request_serializer=mom__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.Publish = channel.unary_unary(
                '/TopicService/Publish',
                request_serializer=mom__pb2.PublishRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.DeleteTopic = channel.unary_unary(
                '/TopicService/DeleteTopic',
                request_serializer=mom__pb2.DeleteRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateTopic = channel.unary_unary(
                '/TopicService/ReplicateTopic',
                request_serializer=mom__pb2.ReplicateTopicRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateSubscription = channel.unary_unary(
                '/TopicService/ReplicateSubscription',
                request_serializer=mom__pb2.ReplicateSubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateMessage = channel.unary_unary(
                '/TopicService/ReplicateMessage',
                request_serializer=mom__pb2.ReplicateMessageRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateUnsubscription = channel.unary_unary(
                '/TopicService/ReplicateUnsubscription',
                request_serializer=mom__pb2.ReplicateUnsubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateTopicDeletion = channel.unary_unary(
                '/TopicService/ReplicateTopicDeletion',
                request_serializer=mom__pb2.ReplicateTopicDeletionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)


class TopicServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Subscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Unsubscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Publish(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTopic(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateTopic(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateUnsubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateTopicDeletion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TopicServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Subscribe': grpc.unary_unary_rpc_method_handler(
                    servicer.Subscribe,
                    request_deserializer=mom__pb2.SubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'Unsubscribe': grpc.unary_unary_rpc_method_handler(
                    servicer.Unsubscribe,
                    request_deserializer=mom__pb2.SubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'Publish': grpc.unary_unary_rpc_method_handler(
                    servicer.Publish,
                    request_deserializer=mom__pb2.PublishRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'DeleteTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTopic,
                    request_deserializer=mom__pb2.DeleteRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateTopic,
                    request_deserializer=mom__pb2.ReplicateTopicRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateSubscription,
                    request_deserializer=mom__pb2.ReplicateSubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateMessage,
                    request_deserializer=mom__pb2.ReplicateMessageRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateUnsubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateUnsubscription,
                    request_deserializer=mom__pb2.ReplicateUnsubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateTopicDeletion': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateTopicDeletion,
                    request_deserializer=mom__pb2.ReplicateTopicDeletionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TopicService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('TopicService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TopicService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Subscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/Subscribe',
            mom__pb2.SubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Unsubscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/Unsubscribe',
            mom__pb2.SubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Publish(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/Publish',
            mom__pb2.PublishRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/DeleteTopic',
            mom__pb2.DeleteRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/ReplicateTopic',
            mom__pb2.ReplicateTopicRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/ReplicateSubscription',
            mom__pb2.ReplicateSubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/ReplicateMessage',
            mom__pb2.ReplicateMessageRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateUnsubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/ReplicateUnsubscription',
            mom__pb2.ReplicateUnsubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateTopicDeletion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TopicService/ReplicateTopicDeletion',
            mom__pb2.ReplicateTopicDeletionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class QueueServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateQueue = channel.unary_unary(
                '/QueueService/CreateQueue',
                request_serializer=mom__pb2.QueueRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.SubscribeQueue = channel.unary_unary(
                '/QueueService/SubscribeQueue',
                request_serializer=mom__pb2.QueueSubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.SendMessage = channel.unary_unary(
                '/QueueService/SendMessage',
                request_serializer=mom__pb2.MessageRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReceiveMessage = channel.unary_unary(
                '/QueueService/ReceiveMessage',
                request_serializer=mom__pb2.QueueRequest.SerializeToString,
                response_deserializer=mom__pb2.MessageResponse.FromString,
                _registered_method=True)
        self.DeleteQueue = channel.unary_unary(
                '/QueueService/DeleteQueue',
                request_serializer=mom__pb2.QueueRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.GetQueues = channel.unary_unary(
                '/QueueService/GetQueues',
                request_serializer=mom__pb2.TokenRequest.SerializeToString,
                response_deserializer=mom__pb2.QueueListResponse.FromString,
                _registered_method=True)
        self.UnsubscribeQueue = channel.unary_unary(
                '/QueueService/UnsubscribeQueue',
                request_serializer=mom__pb2.QueueSubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateQueue = channel.unary_unary(
                '/QueueService/ReplicateQueue',
                request_serializer=mom__pb2.ReplicateQueueRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateQueueSubscription = channel.unary_unary(
                '/QueueService/ReplicateQueueSubscription',
                request_serializer=mom__pb2.ReplicateQueueSubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateQueueMessage = channel.unary_unary(
                '/QueueService/ReplicateQueueMessage',
                request_serializer=mom__pb2.ReplicateQueueMessageRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)
        self.ReplicateQueueUnsubscription = channel.unary_unary(
                '/QueueService/ReplicateQueueUnsubscription',
                request_serializer=mom__pb2.ReplicateQueueUnsubscriptionRequest.SerializeToString,
                response_deserializer=mom__pb2.Response.FromString,
                _registered_method=True)


class QueueServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateQueue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeQueue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReceiveMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteQueue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetQueues(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnsubscribeQueue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateQueue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateQueueSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateQueueMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateQueueUnsubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueueServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateQueue': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateQueue,
                    request_deserializer=mom__pb2.QueueRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'SubscribeQueue': grpc.unary_unary_rpc_method_handler(
                    servicer.SubscribeQueue,
                    request_deserializer=mom__pb2.QueueSubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=mom__pb2.MessageRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReceiveMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveMessage,
                    request_deserializer=mom__pb2.QueueRequest.FromString,
                    response_serializer=mom__pb2.MessageResponse.SerializeToString,
            ),
            'DeleteQueue': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteQueue,
                    request_deserializer=mom__pb2.QueueRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'GetQueues': grpc.unary_unary_rpc_method_handler(
                    servicer.GetQueues,
                    request_deserializer=mom__pb2.TokenRequest.FromString,
                    response_serializer=mom__pb2.QueueListResponse.SerializeToString,
            ),
            'UnsubscribeQueue': grpc.unary_unary_rpc_method_handler(
                    servicer.UnsubscribeQueue,
                    request_deserializer=mom__pb2.QueueSubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateQueue': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateQueue,
                    request_deserializer=mom__pb2.ReplicateQueueRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateQueueSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateQueueSubscription,
                    request_deserializer=mom__pb2.ReplicateQueueSubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateQueueMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateQueueMessage,
                    request_deserializer=mom__pb2.ReplicateQueueMessageRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
            'ReplicateQueueUnsubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateQueueUnsubscription,
                    request_deserializer=mom__pb2.ReplicateQueueUnsubscriptionRequest.FromString,
                    response_serializer=mom__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'QueueService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('QueueService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class QueueService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateQueue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/CreateQueue',
            mom__pb2.QueueRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribeQueue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/SubscribeQueue',
            mom__pb2.QueueSubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/SendMessage',
            mom__pb2.MessageRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReceiveMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/ReceiveMessage',
            mom__pb2.QueueRequest.SerializeToString,
            mom__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteQueue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/DeleteQueue',
            mom__pb2.QueueRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetQueues(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/GetQueues',
            mom__pb2.TokenRequest.SerializeToString,
            mom__pb2.QueueListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UnsubscribeQueue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/UnsubscribeQueue',
            mom__pb2.QueueSubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateQueue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/ReplicateQueue',
            mom__pb2.ReplicateQueueRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateQueueSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/ReplicateQueueSubscription',
            mom__pb2.ReplicateQueueSubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateQueueMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/ReplicateQueueMessage',
            mom__pb2.ReplicateQueueMessageRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateQueueUnsubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/QueueService/ReplicateQueueUnsubscription',
            mom__pb2.ReplicateQueueUnsubscriptionRequest.SerializeToString,
            mom__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
