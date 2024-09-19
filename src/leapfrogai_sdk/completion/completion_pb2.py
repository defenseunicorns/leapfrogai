# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: leapfrogai_sdk/completion/completion.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*leapfrogai_sdk/completion/completion.proto\x12\ncompletion\"\xf7\x06\n\x11\x43ompletionRequest\x12\x0e\n\x06prompt\x18\x01 \x01(\t\x12\x13\n\x06suffix\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x1b\n\x0emax_new_tokens\x18\x03 \x01(\x05H\x01\x88\x01\x01\x12\x18\n\x0btemperature\x18\x04 \x01(\x02H\x02\x88\x01\x01\x12\x12\n\x05top_k\x18\x05 \x01(\x05H\x03\x88\x01\x01\x12\x12\n\x05top_p\x18\x06 \x01(\x02H\x04\x88\x01\x01\x12\x16\n\tdo_sample\x18\x07 \x01(\x08H\x05\x88\x01\x01\x12\x0e\n\x01n\x18\x08 \x01(\x05H\x06\x88\x01\x01\x12\x15\n\x08logprobs\x18\t \x01(\x05H\x07\x88\x01\x01\x12\x11\n\x04\x65\x63ho\x18\n \x01(\x08H\x08\x88\x01\x01\x12\x0c\n\x04stop\x18\x0b \x03(\t\x12\x1f\n\x12repetition_penalty\x18\x0c \x01(\x02H\t\x88\x01\x01\x12\x1d\n\x10presence_penalty\x18\r \x01(\x02H\n\x88\x01\x01\x12\x1e\n\x11\x66requence_penalty\x18\x0e \x01(\x02H\x0b\x88\x01\x01\x12\x14\n\x07\x62\x65st_of\x18\x0f \x01(\tH\x0c\x88\x01\x01\x12@\n\nlogit_bias\x18\x10 \x03(\x0b\x32,.completion.CompletionRequest.LogitBiasEntry\x12\x1d\n\x10return_full_text\x18\x11 \x01(\x08H\r\x88\x01\x01\x12\x15\n\x08truncate\x18\x12 \x01(\x05H\x0e\x88\x01\x01\x12\x16\n\ttypical_p\x18\x13 \x01(\x02H\x0f\x88\x01\x01\x12\x16\n\twatermark\x18\x14 \x01(\x08H\x10\x88\x01\x01\x12\x11\n\x04seed\x18\x15 \x01(\x05H\x11\x88\x01\x01\x12\x11\n\x04user\x18\x16 \x01(\tH\x12\x88\x01\x01\x1a\x30\n\x0eLogitBiasEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x42\t\n\x07_suffixB\x11\n\x0f_max_new_tokensB\x0e\n\x0c_temperatureB\x08\n\x06_top_kB\x08\n\x06_top_pB\x0c\n\n_do_sampleB\x04\n\x02_nB\x0b\n\t_logprobsB\x07\n\x05_echoB\x15\n\x13_repetition_penaltyB\x13\n\x11_presence_penaltyB\x14\n\x12_frequence_penaltyB\n\n\x08_best_ofB\x13\n\x11_return_full_textB\x0b\n\t_truncateB\x0c\n\n_typical_pB\x0c\n\n_watermarkB\x07\n\x05_seedB\x07\n\x05_user\"j\n\x10\x43ompletionChoice\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\x05\x12\x39\n\rfinish_reason\x18\x03 \x01(\x0e\x32\".completion.CompletionFinishReason\"Y\n\x0f\x43ompletionUsage\x12\x15\n\rprompt_tokens\x18\x01 \x01(\x05\x12\x19\n\x11\x63ompletion_tokens\x18\x02 \x01(\x05\x12\x14\n\x0ctotal_tokens\x18\x03 \x01(\x05\"~\n\x12\x43ompletionResponse\x12-\n\x07\x63hoices\x18\x01 \x03(\x0b\x32\x1c.completion.CompletionChoice\x12/\n\x05usage\x18\x02 \x01(\x0b\x32\x1b.completion.CompletionUsageH\x00\x88\x01\x01\x42\x08\n\x06_usage*8\n\x16\x43ompletionFinishReason\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04STOP\x10\x01\x12\n\n\x06LENGTH\x10\x02\x32^\n\x11\x43ompletionService\x12I\n\x08\x43omplete\x12\x1d.completion.CompletionRequest\x1a\x1e.completion.CompletionResponse2l\n\x17\x43ompletionStreamService\x12Q\n\x0e\x43ompleteStream\x12\x1d.completion.CompletionRequest\x1a\x1e.completion.CompletionResponse0\x01\x42=Z;github.com/defenseunicorns/leapfrogai/pkg/client/completionb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'leapfrogai_sdk.completion.completion_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z;github.com/defenseunicorns/leapfrogai/pkg/client/completion'
  _globals['_COMPLETIONREQUEST_LOGITBIASENTRY']._options = None
  _globals['_COMPLETIONREQUEST_LOGITBIASENTRY']._serialized_options = b'8\001'
  _globals['_COMPLETIONFINISHREASON']._serialized_start=1275
  _globals['_COMPLETIONFINISHREASON']._serialized_end=1331
  _globals['_COMPLETIONREQUEST']._serialized_start=59
  _globals['_COMPLETIONREQUEST']._serialized_end=946
  _globals['_COMPLETIONREQUEST_LOGITBIASENTRY']._serialized_start=632
  _globals['_COMPLETIONREQUEST_LOGITBIASENTRY']._serialized_end=680
  _globals['_COMPLETIONCHOICE']._serialized_start=948
  _globals['_COMPLETIONCHOICE']._serialized_end=1054
  _globals['_COMPLETIONUSAGE']._serialized_start=1056
  _globals['_COMPLETIONUSAGE']._serialized_end=1145
  _globals['_COMPLETIONRESPONSE']._serialized_start=1147
  _globals['_COMPLETIONRESPONSE']._serialized_end=1273
  _globals['_COMPLETIONSERVICE']._serialized_start=1333
  _globals['_COMPLETIONSERVICE']._serialized_end=1427
  _globals['_COMPLETIONSTREAMSERVICE']._serialized_start=1429
  _globals['_COMPLETIONSTREAMSERVICE']._serialized_end=1537
# @@protoc_insertion_point(module_scope)
