# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: generate/generate.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17generate/generate.proto\x12\x08generate\"\xec\x02\n\x11\x43ompletionRequest\x12\x0e\n\x06prompt\x18\x01 \x01(\t\x12\x0e\n\x06suffix\x18\x02 \x01(\t\x12\x12\n\nmax_tokens\x18\x03 \x01(\x05\x12\x13\n\x0btemperature\x18\x04 \x01(\x02\x12\r\n\x05top_p\x18\x05 \x01(\x02\x12\t\n\x01n\x18\x06 \x01(\x05\x12\x0e\n\x06stream\x18\x07 \x01(\x08\x12\x10\n\x08logprobs\x18\x08 \x01(\x05\x12\x0c\n\x04\x65\x63ho\x18\t \x01(\x08\x12\x0c\n\x04stop\x18\n \x01(\t\x12\x18\n\x10presence_penalty\x18\x0b \x01(\x02\x12\x19\n\x11\x66requence_penalty\x18\x0c \x01(\x02\x12\x0f\n\x07\x62\x65st_of\x18\r \x01(\x05\x12>\n\nlogit_bias\x18\x0e \x03(\x0b\x32*.generate.CompletionRequest.LogitBiasEntry\x1a\x30\n\x0eLogitBiasEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"(\n\x12\x43ompletionResponse\x12\x12\n\ncompletion\x18\x01 \x01(\t2Z\n\x11\x43ompletionService\x12\x45\n\x08\x43omplete\x12\x1b.generate.CompletionRequest\x1a\x1c.generate.CompletionResponseB;Z9github.com/defenseunicorns/leapfrogai/pkg/client/generateb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'generate.generate_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z9github.com/defenseunicorns/leapfrogai/pkg/client/generate'
  _COMPLETIONREQUEST_LOGITBIASENTRY._options = None
  _COMPLETIONREQUEST_LOGITBIASENTRY._serialized_options = b'8\001'
  _COMPLETIONREQUEST._serialized_start=38
  _COMPLETIONREQUEST._serialized_end=402
  _COMPLETIONREQUEST_LOGITBIASENTRY._serialized_start=354
  _COMPLETIONREQUEST_LOGITBIASENTRY._serialized_end=402
  _COMPLETIONRESPONSE._serialized_start=404
  _COMPLETIONRESPONSE._serialized_end=444
  _COMPLETIONSERVICE._serialized_start=446
  _COMPLETIONSERVICE._serialized_end=536
# @@protoc_insertion_point(module_scope)
