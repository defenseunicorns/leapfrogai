# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: leapfrogai_sdk/embeddings/embeddings.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n*leapfrogai_sdk/embeddings/embeddings.proto\x12\nembeddings""\n\x10\x45mbeddingRequest\x12\x0e\n\x06inputs\x18\x01 \x03(\t"\x1e\n\tEmbedding\x12\x11\n\tembedding\x18\x01 \x03(\x02">\n\x11\x45mbeddingResponse\x12)\n\nembeddings\x18\x01 \x03(\x0b\x32\x15.embeddings.Embedding2c\n\x11\x45mbeddingsService\x12N\n\x0f\x43reateEmbedding\x12\x1c.embeddings.EmbeddingRequest\x1a\x1d.embeddings.EmbeddingResponseB=Z;github.com/defenseunicorns/leapfrogai/pkg/client/embeddingsb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "leapfrogai_sdk.embeddings.embeddings_pb2", _globals
)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals["DESCRIPTOR"]._serialized_options = (
        b"Z;github.com/defenseunicorns/leapfrogai/pkg/client/embeddings"
    )
    _globals["_EMBEDDINGREQUEST"]._serialized_start = 58
    _globals["_EMBEDDINGREQUEST"]._serialized_end = 92
    _globals["_EMBEDDING"]._serialized_start = 94
    _globals["_EMBEDDING"]._serialized_end = 124
    _globals["_EMBEDDINGRESPONSE"]._serialized_start = 126
    _globals["_EMBEDDINGRESPONSE"]._serialized_end = 188
    _globals["_EMBEDDINGSSERVICE"]._serialized_start = 190
    _globals["_EMBEDDINGSSERVICE"]._serialized_end = 289
# @@protoc_insertion_point(module_scope)
