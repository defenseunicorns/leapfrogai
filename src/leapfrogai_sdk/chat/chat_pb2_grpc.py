# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from leapfrogai_sdk.chat import chat_pb2 as leapfrogai__sdk_dot_chat_dot_chat__pb2


class ChatCompletionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ChatComplete = channel.unary_unary(
            "/chat.ChatCompletionService/ChatComplete",
            request_serializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionRequest.SerializeToString,
            response_deserializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionResponse.FromString,
        )


class ChatCompletionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ChatComplete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ChatCompletionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ChatComplete": grpc.unary_unary_rpc_method_handler(
            servicer.ChatComplete,
            request_deserializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionRequest.FromString,
            response_serializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "chat.ChatCompletionService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ChatCompletionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ChatComplete(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chat.ChatCompletionService/ChatComplete",
            leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionRequest.SerializeToString,
            leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )


class ChatCompletionStreamServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ChatCompleteStream = channel.unary_stream(
            "/chat.ChatCompletionStreamService/ChatCompleteStream",
            request_serializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionRequest.SerializeToString,
            response_deserializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionResponse.FromString,
        )


class ChatCompletionStreamServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ChatCompleteStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ChatCompletionStreamServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ChatCompleteStream": grpc.unary_stream_rpc_method_handler(
            servicer.ChatCompleteStream,
            request_deserializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionRequest.FromString,
            response_serializer=leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "chat.ChatCompletionStreamService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ChatCompletionStreamService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ChatCompleteStream(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/chat.ChatCompletionStreamService/ChatCompleteStream",
            leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionRequest.SerializeToString,
            leapfrogai__sdk_dot_chat_dot_chat__pb2.ChatCompletionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
