# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from leapfrogai_sdk.audio import audio_pb2 as leapfrogai__sdk_dot_audio_dot_audio__pb2


class AudioStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Translate = channel.stream_unary(
            "/audio.Audio/Translate",
            request_serializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioRequest.SerializeToString,
            response_deserializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioResponse.FromString,
        )
        self.Transcribe = channel.stream_unary(
            "/audio.Audio/Transcribe",
            request_serializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioRequest.SerializeToString,
            response_deserializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioResponse.FromString,
        )


class AudioServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Translate(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Transcribe(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_AudioServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Translate": grpc.stream_unary_rpc_method_handler(
            servicer.Translate,
            request_deserializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioRequest.FromString,
            response_serializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioResponse.SerializeToString,
        ),
        "Transcribe": grpc.stream_unary_rpc_method_handler(
            servicer.Transcribe,
            request_deserializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioRequest.FromString,
            response_serializer=leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "audio.Audio", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Audio(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Translate(
        request_iterator,
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
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            "/audio.Audio/Translate",
            leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioRequest.SerializeToString,
            leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Transcribe(
        request_iterator,
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
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            "/audio.Audio/Transcribe",
            leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioRequest.SerializeToString,
            leapfrogai__sdk_dot_audio_dot_audio__pb2.AudioResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
