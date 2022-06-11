"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import ory.keto.acl.v1alpha1.acl_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class CheckRequest(google.protobuf.message.Message):
    """The request for a CheckService.Check RPC.
    Checks whether a specific subject is related to an object.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAMESPACE_FIELD_NUMBER: builtins.int
    OBJECT_FIELD_NUMBER: builtins.int
    RELATION_FIELD_NUMBER: builtins.int
    SUBJECT_FIELD_NUMBER: builtins.int
    LATEST_FIELD_NUMBER: builtins.int
    SNAPTOKEN_FIELD_NUMBER: builtins.int
    MAX_DEPTH_FIELD_NUMBER: builtins.int
    namespace: typing.Text
    """The namespace to evaluate the check.

    Note: If you use the expand-API and the check
    evaluates a RelationTuple specifying a SubjectSet as
    subject or due to a rewrite rule in a namespace config
    this check request may involve other namespaces automatically.
    """

    object: typing.Text
    """The related object in this check."""

    relation: typing.Text
    """The relation between the Object and the Subject."""

    @property
    def subject(self) -> ory.keto.acl.v1alpha1.acl_pb2.Subject:
        """The related subject in this check."""
        pass
    latest: builtins.bool
    """This field is not implemented yet and has no effect.
    <!--
    Set this field to `true` in case your application
    needs to authorize depending on up to date ACLs,
    also called a "content-change check".

    If set to `true` the `snaptoken` field is ignored,
    the check is evaluated at the latest snapshot
    (globally consistent) and the response includes a
    snaptoken for clients to store along with object
    contents that can be used for subsequent checks
    of the same content version.

    Example use case:
     - You need to authorize a user to modify/delete some resource
       and it is unacceptable that if the permission to do that had
       just been revoked some seconds ago so that the change had not
       yet been fully replicated to all availability zones.
    -->
    """

    snaptoken: typing.Text
    """This field is not implemented yet and has no effect.
    <!--
    Optional. Like reads, a check is always evaluated at a
    consistent snapshot no earlier than the given snaptoken.

    Leave this field blank if you want to evaluate the check
    based on eventually consistent ACLs, benefiting from very
    low latency, but possibly slightly stale results.

    If the specified token is too old and no longer known,
    the server falls back as if no snaptoken had been specified.

    If not specified the server tries to evaluate the check
    on the best snapshot version where it is very likely that
    ACLs had already been replicated to all availability zones.
    -->
    """

    max_depth: builtins.int
    """The maximum depth to search for a relation.

    If the value is less than 1 or greater than the global
    max-depth then the global max-depth will be used instead.
    """

    def __init__(
        self,
        *,
        namespace: typing.Text = ...,
        object: typing.Text = ...,
        relation: typing.Text = ...,
        subject: typing.Optional[ory.keto.acl.v1alpha1.acl_pb2.Subject] = ...,
        latest: builtins.bool = ...,
        snaptoken: typing.Text = ...,
        max_depth: builtins.int = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["subject", b"subject"]
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "latest",
            b"latest",
            "max_depth",
            b"max_depth",
            "namespace",
            b"namespace",
            "object",
            b"object",
            "relation",
            b"relation",
            "snaptoken",
            b"snaptoken",
            "subject",
            b"subject",
        ],
    ) -> None: ...

global___CheckRequest = CheckRequest

class CheckResponse(google.protobuf.message.Message):
    """The response for a CheckService.Check rpc."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ALLOWED_FIELD_NUMBER: builtins.int
    SNAPTOKEN_FIELD_NUMBER: builtins.int
    allowed: builtins.bool
    """Whether the specified subject (id)
    is related to the requested object.

    It is false by default if no ACL matches.
    """

    snaptoken: typing.Text
    """This field is not implemented yet and has no effect.
    <!--
    The last known snapshot token ONLY specified if
    the request had not specified a snaptoken,
    since this performed a "content-change request"
    and consistently fetched the last known snapshot token.

    This field is not set if the request had specified a snaptoken!

    If set, clients should cache and use this token
    for subsequent requests to have minimal latency,
    but allow slightly stale responses (only some milliseconds or seconds).
    -->
    """

    def __init__(
        self,
        *,
        allowed: builtins.bool = ...,
        snaptoken: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "allowed", b"allowed", "snaptoken", b"snaptoken"
        ],
    ) -> None: ...

global___CheckResponse = CheckResponse