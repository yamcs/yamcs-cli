# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: security.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='security.proto',
  package='',
  syntax='proto2',
  serialized_options=_b('\n\033org.yamcs.security.protobufB\rSecurityProtoP\001'),
  serialized_pb=_b('\n\x0esecurity.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"A\n\x11\x41\x63\x63ountCollection\x12\x0b\n\x03seq\x18\x01 \x01(\x05\x12\x1f\n\x07records\x18\x02 \x03(\x0b\x32\x0e.AccountRecord\"\xf1\x02\n\rAccountRecord\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64isplayName\x18\x03 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x04 \x01(\x08\x12\x11\n\tcreatedBy\x18\x05 \x01(\x05\x12\x30\n\x0c\x63reationTime\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x34\n\x10\x63onfirmationTime\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rlastLoginTime\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nuserDetail\x18\t \x01(\x0b\x32\x18.UserAccountRecordDetailH\x00\x12\x34\n\rserviceDetail\x18\n \x01(\x0b\x32\x1b.ServiceAccountRecordDetailH\x00\x42\r\n\x0b\x61\x63\x63ountType\"\x9e\x01\n\x17UserAccountRecordDetail\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0c\n\x04hash\x18\x02 \x01(\t\x12\x11\n\tsuperuser\x18\x03 \x01(\x08\x12\r\n\x05roles\x18\x05 \x03(\t\x12%\n\nidentities\x18\x04 \x03(\x0b\x32\x11.ExternalIdentity\x12\x1d\n\tclearance\x18\x06 \x01(\x0b\x32\n.Clearance\"L\n\x1aServiceAccountRecordDetail\x12\x15\n\rapplicationId\x18\x01 \x01(\t\x12\x17\n\x0f\x61pplicationHash\x18\x02 \x01(\t\"6\n\x10\x45xternalIdentity\x12\x10\n\x08identity\x18\x01 \x01(\t\x12\x10\n\x08provider\x18\x02 \x01(\t\"[\n\tClearance\x12\r\n\x05level\x18\x01 \x01(\t\x12\x10\n\x08issuedBy\x18\x02 \x01(\x05\x12-\n\tissueTime\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"=\n\x0fGroupCollection\x12\x0b\n\x03seq\x18\x01 \x01(\x05\x12\x1d\n\x07records\x18\x02 \x03(\x0b\x32\x0c.GroupRecord\"M\n\x0bGroupRecord\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07members\x18\x04 \x03(\x05\"I\n\x15\x41pplicationCollection\x12\x0b\n\x03seq\x18\x01 \x01(\x05\x12#\n\x07records\x18\x02 \x03(\x0b\x32\x12.ApplicationRecord\"\xdb\x01\n\x11\x41pplicationRecord\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x63lientId\x18\x03 \x01(\t\x12\x12\n\nclientHash\x18\x04 \x01(\t\x12\x0e\n\x06scopes\x18\x05 \x03(\t\x12\x11\n\tcreatedBy\x18\x06 \x01(\x05\x12\x30\n\x0c\x63reationTime\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rlastLoginTime\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampB.\n\x1borg.yamcs.security.protobufB\rSecurityProtoP\x01')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_ACCOUNTCOLLECTION = _descriptor.Descriptor(
  name='AccountCollection',
  full_name='AccountCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='seq', full_name='AccountCollection.seq', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='records', full_name='AccountCollection.records', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=51,
  serialized_end=116,
)


_ACCOUNTRECORD = _descriptor.Descriptor(
  name='AccountRecord',
  full_name='AccountRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='AccountRecord.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='AccountRecord.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='displayName', full_name='AccountRecord.displayName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='active', full_name='AccountRecord.active', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='createdBy', full_name='AccountRecord.createdBy', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='creationTime', full_name='AccountRecord.creationTime', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='confirmationTime', full_name='AccountRecord.confirmationTime', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lastLoginTime', full_name='AccountRecord.lastLoginTime', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='userDetail', full_name='AccountRecord.userDetail', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serviceDetail', full_name='AccountRecord.serviceDetail', index=9,
      number=10, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='accountType', full_name='AccountRecord.accountType',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=119,
  serialized_end=488,
)


_USERACCOUNTRECORDDETAIL = _descriptor.Descriptor(
  name='UserAccountRecordDetail',
  full_name='UserAccountRecordDetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='UserAccountRecordDetail.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hash', full_name='UserAccountRecordDetail.hash', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='superuser', full_name='UserAccountRecordDetail.superuser', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='roles', full_name='UserAccountRecordDetail.roles', index=3,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='identities', full_name='UserAccountRecordDetail.identities', index=4,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='clearance', full_name='UserAccountRecordDetail.clearance', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  serialized_start=491,
  serialized_end=649,
)


_SERVICEACCOUNTRECORDDETAIL = _descriptor.Descriptor(
  name='ServiceAccountRecordDetail',
  full_name='ServiceAccountRecordDetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='applicationId', full_name='ServiceAccountRecordDetail.applicationId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='applicationHash', full_name='ServiceAccountRecordDetail.applicationHash', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=651,
  serialized_end=727,
)


_EXTERNALIDENTITY = _descriptor.Descriptor(
  name='ExternalIdentity',
  full_name='ExternalIdentity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='identity', full_name='ExternalIdentity.identity', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='provider', full_name='ExternalIdentity.provider', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=729,
  serialized_end=783,
)


_CLEARANCE = _descriptor.Descriptor(
  name='Clearance',
  full_name='Clearance',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='level', full_name='Clearance.level', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issuedBy', full_name='Clearance.issuedBy', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issueTime', full_name='Clearance.issueTime', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=785,
  serialized_end=876,
)


_GROUPCOLLECTION = _descriptor.Descriptor(
  name='GroupCollection',
  full_name='GroupCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='seq', full_name='GroupCollection.seq', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='records', full_name='GroupCollection.records', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=878,
  serialized_end=939,
)


_GROUPRECORD = _descriptor.Descriptor(
  name='GroupRecord',
  full_name='GroupRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='GroupRecord.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='GroupRecord.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='GroupRecord.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='members', full_name='GroupRecord.members', index=3,
      number=4, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=941,
  serialized_end=1018,
)


_APPLICATIONCOLLECTION = _descriptor.Descriptor(
  name='ApplicationCollection',
  full_name='ApplicationCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='seq', full_name='ApplicationCollection.seq', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='records', full_name='ApplicationCollection.records', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1020,
  serialized_end=1093,
)


_APPLICATIONRECORD = _descriptor.Descriptor(
  name='ApplicationRecord',
  full_name='ApplicationRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ApplicationRecord.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='ApplicationRecord.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='clientId', full_name='ApplicationRecord.clientId', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='clientHash', full_name='ApplicationRecord.clientHash', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scopes', full_name='ApplicationRecord.scopes', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='createdBy', full_name='ApplicationRecord.createdBy', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='creationTime', full_name='ApplicationRecord.creationTime', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lastLoginTime', full_name='ApplicationRecord.lastLoginTime', index=7,
      number=8, type=11, cpp_type=10, label=1,
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
  serialized_start=1096,
  serialized_end=1315,
)

_ACCOUNTCOLLECTION.fields_by_name['records'].message_type = _ACCOUNTRECORD
_ACCOUNTRECORD.fields_by_name['creationTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_ACCOUNTRECORD.fields_by_name['confirmationTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_ACCOUNTRECORD.fields_by_name['lastLoginTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_ACCOUNTRECORD.fields_by_name['userDetail'].message_type = _USERACCOUNTRECORDDETAIL
_ACCOUNTRECORD.fields_by_name['serviceDetail'].message_type = _SERVICEACCOUNTRECORDDETAIL
_ACCOUNTRECORD.oneofs_by_name['accountType'].fields.append(
  _ACCOUNTRECORD.fields_by_name['userDetail'])
_ACCOUNTRECORD.fields_by_name['userDetail'].containing_oneof = _ACCOUNTRECORD.oneofs_by_name['accountType']
_ACCOUNTRECORD.oneofs_by_name['accountType'].fields.append(
  _ACCOUNTRECORD.fields_by_name['serviceDetail'])
_ACCOUNTRECORD.fields_by_name['serviceDetail'].containing_oneof = _ACCOUNTRECORD.oneofs_by_name['accountType']
_USERACCOUNTRECORDDETAIL.fields_by_name['identities'].message_type = _EXTERNALIDENTITY
_USERACCOUNTRECORDDETAIL.fields_by_name['clearance'].message_type = _CLEARANCE
_CLEARANCE.fields_by_name['issueTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GROUPCOLLECTION.fields_by_name['records'].message_type = _GROUPRECORD
_APPLICATIONCOLLECTION.fields_by_name['records'].message_type = _APPLICATIONRECORD
_APPLICATIONRECORD.fields_by_name['creationTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_APPLICATIONRECORD.fields_by_name['lastLoginTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['AccountCollection'] = _ACCOUNTCOLLECTION
DESCRIPTOR.message_types_by_name['AccountRecord'] = _ACCOUNTRECORD
DESCRIPTOR.message_types_by_name['UserAccountRecordDetail'] = _USERACCOUNTRECORDDETAIL
DESCRIPTOR.message_types_by_name['ServiceAccountRecordDetail'] = _SERVICEACCOUNTRECORDDETAIL
DESCRIPTOR.message_types_by_name['ExternalIdentity'] = _EXTERNALIDENTITY
DESCRIPTOR.message_types_by_name['Clearance'] = _CLEARANCE
DESCRIPTOR.message_types_by_name['GroupCollection'] = _GROUPCOLLECTION
DESCRIPTOR.message_types_by_name['GroupRecord'] = _GROUPRECORD
DESCRIPTOR.message_types_by_name['ApplicationCollection'] = _APPLICATIONCOLLECTION
DESCRIPTOR.message_types_by_name['ApplicationRecord'] = _APPLICATIONRECORD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AccountCollection = _reflection.GeneratedProtocolMessageType('AccountCollection', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTCOLLECTION,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:AccountCollection)
  ))
_sym_db.RegisterMessage(AccountCollection)

AccountRecord = _reflection.GeneratedProtocolMessageType('AccountRecord', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTRECORD,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:AccountRecord)
  ))
_sym_db.RegisterMessage(AccountRecord)

UserAccountRecordDetail = _reflection.GeneratedProtocolMessageType('UserAccountRecordDetail', (_message.Message,), dict(
  DESCRIPTOR = _USERACCOUNTRECORDDETAIL,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:UserAccountRecordDetail)
  ))
_sym_db.RegisterMessage(UserAccountRecordDetail)

ServiceAccountRecordDetail = _reflection.GeneratedProtocolMessageType('ServiceAccountRecordDetail', (_message.Message,), dict(
  DESCRIPTOR = _SERVICEACCOUNTRECORDDETAIL,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:ServiceAccountRecordDetail)
  ))
_sym_db.RegisterMessage(ServiceAccountRecordDetail)

ExternalIdentity = _reflection.GeneratedProtocolMessageType('ExternalIdentity', (_message.Message,), dict(
  DESCRIPTOR = _EXTERNALIDENTITY,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:ExternalIdentity)
  ))
_sym_db.RegisterMessage(ExternalIdentity)

Clearance = _reflection.GeneratedProtocolMessageType('Clearance', (_message.Message,), dict(
  DESCRIPTOR = _CLEARANCE,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:Clearance)
  ))
_sym_db.RegisterMessage(Clearance)

GroupCollection = _reflection.GeneratedProtocolMessageType('GroupCollection', (_message.Message,), dict(
  DESCRIPTOR = _GROUPCOLLECTION,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:GroupCollection)
  ))
_sym_db.RegisterMessage(GroupCollection)

GroupRecord = _reflection.GeneratedProtocolMessageType('GroupRecord', (_message.Message,), dict(
  DESCRIPTOR = _GROUPRECORD,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:GroupRecord)
  ))
_sym_db.RegisterMessage(GroupRecord)

ApplicationCollection = _reflection.GeneratedProtocolMessageType('ApplicationCollection', (_message.Message,), dict(
  DESCRIPTOR = _APPLICATIONCOLLECTION,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:ApplicationCollection)
  ))
_sym_db.RegisterMessage(ApplicationCollection)

ApplicationRecord = _reflection.GeneratedProtocolMessageType('ApplicationRecord', (_message.Message,), dict(
  DESCRIPTOR = _APPLICATIONRECORD,
  __module__ = 'security_pb2'
  # @@protoc_insertion_point(class_scope:ApplicationRecord)
  ))
_sym_db.RegisterMessage(ApplicationRecord)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
