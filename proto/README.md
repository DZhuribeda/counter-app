``
python -m grpc_tools.protoc -I../proto --python_out=../counter_app --mypy_out=../counter_app --grpc_python_out=../counter_app ory/keto/acl/v1alpha1/acl.proto ory/keto/acl/v1alpha1/write_service.proto ory/keto/acl/v1alpha1/check_service.proto ory/keto/acl/v1alpha1/read_service.proto ory/keto/acl/v1alpha1/expand_service.proto
```