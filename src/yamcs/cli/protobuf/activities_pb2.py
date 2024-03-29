# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: activities.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='activities.proto',
  package='',
  syntax='proto2',
  serialized_options=b'\n\035org.yamcs.activities.protobufB\017ActivitiesProtoP\001',
  serialized_pb=b'\n\x10\x61\x63tivities.proto\x1a\x1cgoogle/protobuf/struct.proto\"I\n\x12\x41\x63tivityDefinition\x12\x0c\n\x04type\x18\x01 \x01(\t\x12%\n\x04\x61rgs\x18\x02 \x01(\x0b\x32\x17.google.protobuf.StructB2\n\x1dorg.yamcs.activities.protobufB\x0f\x41\x63tivitiesProtoP\x01'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])




_ACTIVITYDEFINITION = _descriptor.Descriptor(
  name='ActivityDefinition',
  full_name='ActivityDefinition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='ActivityDefinition.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='args', full_name='ActivityDefinition.args', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=123,
)

_ACTIVITYDEFINITION.fields_by_name['args'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
DESCRIPTOR.message_types_by_name['ActivityDefinition'] = _ACTIVITYDEFINITION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ActivityDefinition = _reflection.GeneratedProtocolMessageType('ActivityDefinition', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVITYDEFINITION,
  '__module__' : 'activities_pb2'
  # @@protoc_insertion_point(class_scope:ActivityDefinition)
  })
_sym_db.RegisterMessage(ActivityDefinition)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
