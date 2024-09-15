# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: leapfrogai_sdk/audio/audio.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n leapfrogai_sdk/audio/audio.proto\x12\x05\x61udio"\xc4\x01\n\rAudioMetadata\x12\x0e\n\x06prompt\x18\x01 \x01(\t\x12\x13\n\x0btemperature\x18\x02 \x01(\x02\x12\x15\n\rinputlanguage\x18\x03 \x01(\t\x12\x30\n\x06\x66ormat\x18\x04 \x01(\x0e\x32 .audio.AudioMetadata.AudioFormat"E\n\x0b\x41udioFormat\x12\x08\n\x04JSON\x10\x00\x12\x08\n\x04TEXT\x10\x01\x12\x07\n\x03SRT\x10\x02\x12\x10\n\x0cVERBOSE_JSON\x10\x03\x12\x07\n\x03VTT\x10\x04"Y\n\x0c\x41udioRequest\x12(\n\x08metadata\x18\x01 \x01(\x0b\x32\x14.audio.AudioMetadataH\x00\x12\x14\n\nchunk_data\x18\x02 \x01(\x0cH\x00\x42\t\n\x07request"\xe1\x02\n\rAudioResponse\x12\x1e\n\x04task\x18\x01 \x01(\x0e\x32\x10.audio.AudioTask\x12\x10\n\x08language\x18\x02 \x01(\t\x12\x10\n\x08\x64uration\x18\x03 \x01(\x01\x12.\n\x08segments\x18\x04 \x03(\x0b\x32\x1c.audio.AudioResponse.Segment\x12\x0c\n\x04text\x18\x05 \x01(\t\x1a\xcd\x01\n\x07Segment\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04seek\x18\x02 \x01(\x05\x12\r\n\x05start\x18\x03 \x01(\x01\x12\x0b\n\x03\x65nd\x18\x04 \x01(\x01\x12\x0c\n\x04text\x18\x05 \x01(\t\x12\x0e\n\x06tokens\x18\x06 \x03(\x05\x12\x13\n\x0btemperature\x18\x07 \x01(\x01\x12\x13\n\x0b\x61vg_logprob\x18\x08 \x01(\x01\x12\x19\n\x11\x63ompression_ratio\x18\t \x01(\x01\x12\x16\n\x0eno_speech_prob\x18\n \x01(\x01\x12\x11\n\ttransient\x18\x0b \x01(\x08**\n\tAudioTask\x12\x0e\n\nTRANSCRIBE\x10\x00\x12\r\n\tTRANSLATE\x10\x01\x32|\n\x05\x41udio\x12\x38\n\tTranslate\x12\x13.audio.AudioRequest\x1a\x14.audio.AudioResponse(\x01\x12\x39\n\nTranscribe\x12\x13.audio.AudioRequest\x1a\x14.audio.AudioResponse(\x01\x42\x38Z6github.com/defenseunicorns/leapfrogai/pkg/client/audiob\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "leapfrogai_sdk.audio.audio_pb2", _globals
)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"Z6github.com/defenseunicorns/leapfrogai/pkg/client/audio"
    _globals["_AUDIOTASK"]._serialized_start = 689
    _globals["_AUDIOTASK"]._serialized_end = 731
    _globals["_AUDIOMETADATA"]._serialized_start = 44
    _globals["_AUDIOMETADATA"]._serialized_end = 240
    _globals["_AUDIOMETADATA_AUDIOFORMAT"]._serialized_start = 171
    _globals["_AUDIOMETADATA_AUDIOFORMAT"]._serialized_end = 240
    _globals["_AUDIOREQUEST"]._serialized_start = 242
    _globals["_AUDIOREQUEST"]._serialized_end = 331
    _globals["_AUDIORESPONSE"]._serialized_start = 334
    _globals["_AUDIORESPONSE"]._serialized_end = 687
    _globals["_AUDIORESPONSE_SEGMENT"]._serialized_start = 482
    _globals["_AUDIORESPONSE_SEGMENT"]._serialized_end = 687
    _globals["_AUDIO"]._serialized_start = 733
    _globals["_AUDIO"]._serialized_end = 857
# @@protoc_insertion_point(module_scope)
