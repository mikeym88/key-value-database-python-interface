# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: annoucement.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='annoucement.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x11\x61nnoucement.proto\"B\n\x0b\x41nnoucement\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x12\n\nrecipients\x18\x02 \x03(\t\x12\x0f\n\x07message\x18\x03 \x01(\tb\x06proto3')
)




_ANNOUCEMENT = _descriptor.Descriptor(
  name='Annoucement',
  full_name='Annoucement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='Annoucement.sender', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='recipients', full_name='Annoucement.recipients', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='Annoucement.message', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=87,
)

DESCRIPTOR.message_types_by_name['Annoucement'] = _ANNOUCEMENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Annoucement = _reflection.GeneratedProtocolMessageType('Annoucement', (_message.Message,), dict(
  DESCRIPTOR = _ANNOUCEMENT,
  __module__ = 'annoucement_pb2'
  # @@protoc_insertion_point(class_scope:Annoucement)
  ))
_sym_db.RegisterMessage(Annoucement)


# @@protoc_insertion_point(module_scope)