# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0eprotobuf.proto\"\xf6\x01\n\rFieldsMessage\x12\x13\n\x0bint32_field\x18\x01 \x01(\x05\x12\x13\n\x0b\x66loat_field\x18\x02 \x01(\x02\x12\x14\n\x0c\x64ouble_field\x18\x03 \x01(\x01\x12\x12\n\nbool_field\x18\x04 \x01(\x08\x12\x14\n\x0cstring_field\x18\x05 \x01(\t\x12\x13\n\x0b\x62ytes_field\x18\x06 \x01(\x0c\x12\x1d\n\x15repeated_string_field\x18\x07 \x03(\t\x12\x1e\n\x0cnested_field\x18\x08 \x01(\x0b\x32\x08.Account\x12\'\n\x15repeated_nested_field\x18\t \x03(\x0b\x32\x08.Account\"\'\n\x11GetAccountRequest\x12\x12\n\naccount_id\x18\x01 \x01(\t\"P\n\x07\x41\x63\x63ount\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0f\n\x07\x62\x61lance\x18\x02 \x01(\x05\x12\"\n\x08settings\x18\x03 \x01(\x0b\x32\x10.AccountSettings\"$\n\x0f\x41\x63\x63ountSettings\x12\x11\n\tis_public\x18\x01 \x01(\x08\x32o\n\x0fTestCaseService\x12.\n\nTestFields\x12\x0e.FieldsMessage\x1a\x0e.FieldsMessage\"\x00\x12,\n\nGetAccount\x12\x12.GetAccountRequest\x1a\x08.Account\"\x00\x62\x06proto3'
)




_FIELDSMESSAGE = _descriptor.Descriptor(
  name='FieldsMessage',
  full_name='FieldsMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='int32_field', full_name='FieldsMessage.int32_field', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='float_field', full_name='FieldsMessage.float_field', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='double_field', full_name='FieldsMessage.double_field', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bool_field', full_name='FieldsMessage.bool_field', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='string_field', full_name='FieldsMessage.string_field', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bytes_field', full_name='FieldsMessage.bytes_field', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='repeated_string_field', full_name='FieldsMessage.repeated_string_field', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nested_field', full_name='FieldsMessage.nested_field', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='repeated_nested_field', full_name='FieldsMessage.repeated_nested_field', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=19,
  serialized_end=265,
)


_GETACCOUNTREQUEST = _descriptor.Descriptor(
  name='GetAccountRequest',
  full_name='GetAccountRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='GetAccountRequest.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=267,
  serialized_end=306,
)


_ACCOUNT = _descriptor.Descriptor(
  name='Account',
  full_name='Account',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='Account.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='balance', full_name='Account.balance', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='Account.settings', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=308,
  serialized_end=388,
)


_ACCOUNTSETTINGS = _descriptor.Descriptor(
  name='AccountSettings',
  full_name='AccountSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_public', full_name='AccountSettings.is_public', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=390,
  serialized_end=426,
)

_FIELDSMESSAGE.fields_by_name['nested_field'].message_type = _ACCOUNT
_FIELDSMESSAGE.fields_by_name['repeated_nested_field'].message_type = _ACCOUNT
_ACCOUNT.fields_by_name['settings'].message_type = _ACCOUNTSETTINGS
DESCRIPTOR.message_types_by_name['FieldsMessage'] = _FIELDSMESSAGE
DESCRIPTOR.message_types_by_name['GetAccountRequest'] = _GETACCOUNTREQUEST
DESCRIPTOR.message_types_by_name['Account'] = _ACCOUNT
DESCRIPTOR.message_types_by_name['AccountSettings'] = _ACCOUNTSETTINGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FieldsMessage = _reflection.GeneratedProtocolMessageType('FieldsMessage', (_message.Message,), {
  'DESCRIPTOR' : _FIELDSMESSAGE,
  '__module__' : 'protobuf_pb2'
  # @@protoc_insertion_point(class_scope:FieldsMessage)
  })
_sym_db.RegisterMessage(FieldsMessage)

GetAccountRequest = _reflection.GeneratedProtocolMessageType('GetAccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETACCOUNTREQUEST,
  '__module__' : 'protobuf_pb2'
  # @@protoc_insertion_point(class_scope:GetAccountRequest)
  })
_sym_db.RegisterMessage(GetAccountRequest)

Account = _reflection.GeneratedProtocolMessageType('Account', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNT,
  '__module__' : 'protobuf_pb2'
  # @@protoc_insertion_point(class_scope:Account)
  })
_sym_db.RegisterMessage(Account)

AccountSettings = _reflection.GeneratedProtocolMessageType('AccountSettings', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTSETTINGS,
  '__module__' : 'protobuf_pb2'
  # @@protoc_insertion_point(class_scope:AccountSettings)
  })
_sym_db.RegisterMessage(AccountSettings)



_TESTCASESERVICE = _descriptor.ServiceDescriptor(
  name='TestCaseService',
  full_name='TestCaseService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=428,
  serialized_end=539,
  methods=[
  _descriptor.MethodDescriptor(
    name='TestFields',
    full_name='TestCaseService.TestFields',
    index=0,
    containing_service=None,
    input_type=_FIELDSMESSAGE,
    output_type=_FIELDSMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetAccount',
    full_name='TestCaseService.GetAccount',
    index=1,
    containing_service=None,
    input_type=_GETACCOUNTREQUEST,
    output_type=_ACCOUNT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TESTCASESERVICE)

DESCRIPTOR.services_by_name['TestCaseService'] = _TESTCASESERVICE

# @@protoc_insertion_point(module_scope)
