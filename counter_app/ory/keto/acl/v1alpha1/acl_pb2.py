# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ory/keto/acl/v1alpha1/acl.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1fory/keto/acl/v1alpha1/acl.proto\x12\x15ory.keto.acl.v1alpha1"u\n\rRelationTuple\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0e\n\x06object\x18\x02 \x01(\t\x12\x10\n\x08relation\x18\x03 \x01(\t\x12/\n\x07subject\x18\x04 \x01(\x0b\x32\x1e.ory.keto.acl.v1alpha1.Subject"P\n\x07Subject\x12\x0c\n\x02id\x18\x01 \x01(\tH\x00\x12\x30\n\x03set\x18\x02 \x01(\x0b\x32!.ory.keto.acl.v1alpha1.SubjectSetH\x00\x42\x05\n\x03ref"A\n\nSubjectSet\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0e\n\x06object\x18\x02 \x01(\t\x12\x10\n\x08relation\x18\x03 \x01(\tB\x8b\x01\n\x18sh.ory.keto.acl.v1alpha1B\x08\x41\x63lProtoP\x01Z3github.com/ory/keto/proto/ory/keto/acl/v1alpha1;acl\xaa\x02\x15Ory.Keto.Acl.V1Alpha1\xca\x02\x15Ory\\Keto\\Acl\\V1alpha1b\x06proto3'
)


_RELATIONTUPLE = DESCRIPTOR.message_types_by_name["RelationTuple"]
_SUBJECT = DESCRIPTOR.message_types_by_name["Subject"]
_SUBJECTSET = DESCRIPTOR.message_types_by_name["SubjectSet"]
RelationTuple = _reflection.GeneratedProtocolMessageType(
    "RelationTuple",
    (_message.Message,),
    {
        "DESCRIPTOR": _RELATIONTUPLE,
        "__module__": "ory.keto.acl.v1alpha1.acl_pb2"
        # @@protoc_insertion_point(class_scope:ory.keto.acl.v1alpha1.RelationTuple)
    },
)
_sym_db.RegisterMessage(RelationTuple)

Subject = _reflection.GeneratedProtocolMessageType(
    "Subject",
    (_message.Message,),
    {
        "DESCRIPTOR": _SUBJECT,
        "__module__": "ory.keto.acl.v1alpha1.acl_pb2"
        # @@protoc_insertion_point(class_scope:ory.keto.acl.v1alpha1.Subject)
    },
)
_sym_db.RegisterMessage(Subject)

SubjectSet = _reflection.GeneratedProtocolMessageType(
    "SubjectSet",
    (_message.Message,),
    {
        "DESCRIPTOR": _SUBJECTSET,
        "__module__": "ory.keto.acl.v1alpha1.acl_pb2"
        # @@protoc_insertion_point(class_scope:ory.keto.acl.v1alpha1.SubjectSet)
    },
)
_sym_db.RegisterMessage(SubjectSet)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\030sh.ory.keto.acl.v1alpha1B\010AclProtoP\001Z3github.com/ory/keto/proto/ory/keto/acl/v1alpha1;acl\252\002\025Ory.Keto.Acl.V1Alpha1\312\002\025Ory\\Keto\\Acl\\V1alpha1"
    _RELATIONTUPLE._serialized_start = 58
    _RELATIONTUPLE._serialized_end = 175
    _SUBJECT._serialized_start = 177
    _SUBJECT._serialized_end = 257
    _SUBJECTSET._serialized_start = 259
    _SUBJECTSET._serialized_end = 324
# @@protoc_insertion_point(module_scope)