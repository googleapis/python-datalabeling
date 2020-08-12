# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async
from google.api_core import operations_v1
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.datalabeling_v1beta1.services.data_labeling_service import (
    DataLabelingServiceAsyncClient,
)
from google.cloud.datalabeling_v1beta1.services.data_labeling_service import (
    DataLabelingServiceClient,
)
from google.cloud.datalabeling_v1beta1.services.data_labeling_service import pagers
from google.cloud.datalabeling_v1beta1.services.data_labeling_service import transports
from google.cloud.datalabeling_v1beta1.types import annotation
from google.cloud.datalabeling_v1beta1.types import annotation_spec_set
from google.cloud.datalabeling_v1beta1.types import (
    annotation_spec_set as gcd_annotation_spec_set,
)
from google.cloud.datalabeling_v1beta1.types import data_labeling_service
from google.cloud.datalabeling_v1beta1.types import data_payloads
from google.cloud.datalabeling_v1beta1.types import dataset
from google.cloud.datalabeling_v1beta1.types import dataset as gcd_dataset
from google.cloud.datalabeling_v1beta1.types import evaluation
from google.cloud.datalabeling_v1beta1.types import evaluation_job
from google.cloud.datalabeling_v1beta1.types import evaluation_job as gcd_evaluation_job
from google.cloud.datalabeling_v1beta1.types import human_annotation_config
from google.cloud.datalabeling_v1beta1.types import instruction
from google.cloud.datalabeling_v1beta1.types import instruction as gcd_instruction
from google.cloud.datalabeling_v1beta1.types import operations
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2 as any  # type: ignore
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert DataLabelingServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        DataLabelingServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataLabelingServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataLabelingServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataLabelingServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataLabelingServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [DataLabelingServiceClient, DataLabelingServiceAsyncClient]
)
def test_data_labeling_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "datalabeling.googleapis.com:443"


def test_data_labeling_service_client_get_transport_class():
    transport = DataLabelingServiceClient.get_transport_class()
    assert transport == transports.DataLabelingServiceGrpcTransport

    transport = DataLabelingServiceClient.get_transport_class("grpc")
    assert transport == transports.DataLabelingServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            DataLabelingServiceClient,
            transports.DataLabelingServiceGrpcTransport,
            "grpc",
        ),
        (
            DataLabelingServiceAsyncClient,
            transports.DataLabelingServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DataLabelingServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataLabelingServiceClient),
)
@mock.patch.object(
    DataLabelingServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataLabelingServiceAsyncClient),
)
def test_data_labeling_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataLabelingServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataLabelingServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=client_cert_source_callback,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_MTLS_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            DataLabelingServiceClient,
            transports.DataLabelingServiceGrpcTransport,
            "grpc",
        ),
        (
            DataLabelingServiceAsyncClient,
            transports.DataLabelingServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_data_labeling_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            DataLabelingServiceClient,
            transports.DataLabelingServiceGrpcTransport,
            "grpc",
        ),
        (
            DataLabelingServiceAsyncClient,
            transports.DataLabelingServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_data_labeling_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


def test_data_labeling_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.datalabeling_v1beta1.services.data_labeling_service.transports.DataLabelingServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataLabelingServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )


def test_create_dataset(
    transport: str = "grpc", request_type=data_labeling_service.CreateDatasetRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            blocking_resources=["blocking_resources_value"],
            data_item_count=1584,
        )

        response = client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.CreateDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_dataset.Dataset)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]

    assert response.data_item_count == 1584


def test_create_dataset_from_dict():
    test_create_dataset(request_type=dict)


@pytest.mark.asyncio
async def test_create_dataset_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.CreateDatasetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                blocking_resources=["blocking_resources_value"],
                data_item_count=1584,
            )
        )

        response = await client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_dataset.Dataset)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]

    assert response.data_item_count == 1584


def test_create_dataset_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateDatasetRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_dataset), "__call__") as call:
        call.return_value = gcd_dataset.Dataset()

        client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_dataset_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateDatasetRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_dataset), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcd_dataset.Dataset())

        await client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_dataset_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_dataset.Dataset()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_dataset(
            parent="parent_value", dataset=gcd_dataset.Dataset(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].dataset == gcd_dataset.Dataset(name="name_value")


def test_create_dataset_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dataset(
            data_labeling_service.CreateDatasetRequest(),
            parent="parent_value",
            dataset=gcd_dataset.Dataset(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_dataset_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcd_dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_dataset(
            parent="parent_value", dataset=gcd_dataset.Dataset(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].dataset == gcd_dataset.Dataset(name="name_value")


@pytest.mark.asyncio
async def test_create_dataset_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_dataset(
            data_labeling_service.CreateDatasetRequest(),
            parent="parent_value",
            dataset=gcd_dataset.Dataset(name="name_value"),
        )


def test_get_dataset(
    transport: str = "grpc", request_type=data_labeling_service.GetDatasetRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            blocking_resources=["blocking_resources_value"],
            data_item_count=1584,
        )

        response = client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Dataset)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]

    assert response.data_item_count == 1584


def test_get_dataset_from_dict():
    test_get_dataset(request_type=dict)


@pytest.mark.asyncio
async def test_get_dataset_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetDatasetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                blocking_resources=["blocking_resources_value"],
                data_item_count=1584,
            )
        )

        response = await client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Dataset)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]

    assert response.data_item_count == 1584


def test_get_dataset_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_dataset), "__call__") as call:
        call.return_value = dataset.Dataset()

        client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_dataset_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_dataset), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Dataset())

        await client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_dataset_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_dataset_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dataset(
            data_labeling_service.GetDatasetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_dataset_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_dataset_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_dataset(
            data_labeling_service.GetDatasetRequest(), name="name_value",
        )


def test_list_datasets(
    transport: str = "grpc", request_type=data_labeling_service.ListDatasetsRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListDatasetsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ListDatasetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_datasets_from_dict():
    test_list_datasets(request_type=dict)


@pytest.mark.asyncio
async def test_list_datasets_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ListDatasetsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_datasets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListDatasetsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_datasets_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListDatasetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_datasets), "__call__") as call:
        call.return_value = data_labeling_service.ListDatasetsResponse()

        client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_datasets_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListDatasetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_datasets), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListDatasetsResponse()
        )

        await client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_datasets_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListDatasetsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_datasets(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_datasets_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_datasets(
            data_labeling_service.ListDatasetsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_datasets_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_datasets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListDatasetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListDatasetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_datasets(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_datasets_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_datasets(
            data_labeling_service.ListDatasetsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_datasets_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_datasets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_datasets(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dataset.Dataset) for i in results)


def test_list_datasets_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_datasets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_datasets(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_datasets_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_datasets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_datasets(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataset.Dataset) for i in responses)


@pytest.mark.asyncio
async def test_list_datasets_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_datasets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_datasets(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_dataset(
    transport: str = "grpc", request_type=data_labeling_service.DeleteDatasetRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.DeleteDatasetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_dataset_from_dict():
    test_delete_dataset(request_type=dict)


@pytest.mark.asyncio
async def test_delete_dataset_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.DeleteDatasetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_dataset_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_dataset), "__call__") as call:
        call.return_value = None

        client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_dataset_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_dataset), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_dataset_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_dataset_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dataset(
            data_labeling_service.DeleteDatasetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_dataset_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_dataset_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_dataset(
            data_labeling_service.DeleteDatasetRequest(), name="name_value",
        )


def test_import_data(
    transport: str = "grpc", request_type=data_labeling_service.ImportDataRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.import_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ImportDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_data_from_dict():
    test_import_data(request_type=dict)


@pytest.mark.asyncio
async def test_import_data_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ImportDataRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.import_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_data_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ImportDataRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.import_data), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_data_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ImportDataRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.import_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_import_data_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.import_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.import_data(
            name="name_value",
            input_config=dataset.InputConfig(
                text_metadata=dataset.TextMetadata(language_code="language_code_value")
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].input_config == dataset.InputConfig(
            text_metadata=dataset.TextMetadata(language_code="language_code_value")
        )


def test_import_data_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.import_data(
            data_labeling_service.ImportDataRequest(),
            name="name_value",
            input_config=dataset.InputConfig(
                text_metadata=dataset.TextMetadata(language_code="language_code_value")
            ),
        )


@pytest.mark.asyncio
async def test_import_data_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.import_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.import_data(
            name="name_value",
            input_config=dataset.InputConfig(
                text_metadata=dataset.TextMetadata(language_code="language_code_value")
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].input_config == dataset.InputConfig(
            text_metadata=dataset.TextMetadata(language_code="language_code_value")
        )


@pytest.mark.asyncio
async def test_import_data_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.import_data(
            data_labeling_service.ImportDataRequest(),
            name="name_value",
            input_config=dataset.InputConfig(
                text_metadata=dataset.TextMetadata(language_code="language_code_value")
            ),
        )


def test_export_data(
    transport: str = "grpc", request_type=data_labeling_service.ExportDataRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.export_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ExportDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_data_from_dict():
    test_export_data(request_type=dict)


@pytest.mark.asyncio
async def test_export_data_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ExportDataRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_data_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ExportDataRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.export_data), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_data_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ExportDataRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_export_data_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.export_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_data(
            name="name_value",
            annotated_dataset="annotated_dataset_value",
            filter="filter_value",
            output_config=dataset.OutputConfig(
                gcs_destination=dataset.GcsDestination(output_uri="output_uri_value")
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].annotated_dataset == "annotated_dataset_value"

        assert args[0].filter == "filter_value"

        assert args[0].output_config == dataset.OutputConfig(
            gcs_destination=dataset.GcsDestination(output_uri="output_uri_value")
        )


def test_export_data_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_data(
            data_labeling_service.ExportDataRequest(),
            name="name_value",
            annotated_dataset="annotated_dataset_value",
            filter="filter_value",
            output_config=dataset.OutputConfig(
                gcs_destination=dataset.GcsDestination(output_uri="output_uri_value")
            ),
        )


@pytest.mark.asyncio
async def test_export_data_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.export_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_data(
            name="name_value",
            annotated_dataset="annotated_dataset_value",
            filter="filter_value",
            output_config=dataset.OutputConfig(
                gcs_destination=dataset.GcsDestination(output_uri="output_uri_value")
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].annotated_dataset == "annotated_dataset_value"

        assert args[0].filter == "filter_value"

        assert args[0].output_config == dataset.OutputConfig(
            gcs_destination=dataset.GcsDestination(output_uri="output_uri_value")
        )


@pytest.mark.asyncio
async def test_export_data_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_data(
            data_labeling_service.ExportDataRequest(),
            name="name_value",
            annotated_dataset="annotated_dataset_value",
            filter="filter_value",
            output_config=dataset.OutputConfig(
                gcs_destination=dataset.GcsDestination(output_uri="output_uri_value")
            ),
        )


def test_get_data_item(
    transport: str = "grpc", request_type=data_labeling_service.GetDataItemRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_data_item), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.DataItem(
            name="name_value",
            image_payload=data_payloads.ImagePayload(mime_type="mime_type_value"),
        )

        response = client.get_data_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetDataItemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.DataItem)

    assert response.name == "name_value"


def test_get_data_item_from_dict():
    test_get_data_item(request_type=dict)


@pytest.mark.asyncio
async def test_get_data_item_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetDataItemRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_data_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.DataItem(name="name_value",)
        )

        response = await client.get_data_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.DataItem)

    assert response.name == "name_value"


def test_get_data_item_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetDataItemRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_data_item), "__call__") as call:
        call.return_value = dataset.DataItem()

        client.get_data_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_data_item_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetDataItemRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_data_item), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.DataItem())

        await client.get_data_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_data_item_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_data_item), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.DataItem()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_data_item(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_data_item_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_data_item(
            data_labeling_service.GetDataItemRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_data_item_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_data_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.DataItem()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.DataItem())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_data_item(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_data_item_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_data_item(
            data_labeling_service.GetDataItemRequest(), name="name_value",
        )


def test_list_data_items(
    transport: str = "grpc", request_type=data_labeling_service.ListDataItemsRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_data_items), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListDataItemsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_data_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ListDataItemsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDataItemsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_data_items_from_dict():
    test_list_data_items(request_type=dict)


@pytest.mark.asyncio
async def test_list_data_items_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ListDataItemsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_data_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListDataItemsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_data_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDataItemsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_data_items_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListDataItemsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_data_items), "__call__") as call:
        call.return_value = data_labeling_service.ListDataItemsResponse()

        client.list_data_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_data_items_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListDataItemsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_data_items), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListDataItemsResponse()
        )

        await client.list_data_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_data_items_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_data_items), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListDataItemsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_data_items(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_data_items_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_data_items(
            data_labeling_service.ListDataItemsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_data_items_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_data_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListDataItemsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListDataItemsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_data_items(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_data_items_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_data_items(
            data_labeling_service.ListDataItemsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_data_items_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_data_items), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDataItemsResponse(
                data_items=[
                    dataset.DataItem(),
                    dataset.DataItem(),
                    dataset.DataItem(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[], next_page_token="def",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(), dataset.DataItem(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_data_items(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dataset.DataItem) for i in results)


def test_list_data_items_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_data_items), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDataItemsResponse(
                data_items=[
                    dataset.DataItem(),
                    dataset.DataItem(),
                    dataset.DataItem(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[], next_page_token="def",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(), dataset.DataItem(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_data_items(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_data_items_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_data_items),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDataItemsResponse(
                data_items=[
                    dataset.DataItem(),
                    dataset.DataItem(),
                    dataset.DataItem(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[], next_page_token="def",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(), dataset.DataItem(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_data_items(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataset.DataItem) for i in responses)


@pytest.mark.asyncio
async def test_list_data_items_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_data_items),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListDataItemsResponse(
                data_items=[
                    dataset.DataItem(),
                    dataset.DataItem(),
                    dataset.DataItem(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[], next_page_token="def",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(),], next_page_token="ghi",
            ),
            data_labeling_service.ListDataItemsResponse(
                data_items=[dataset.DataItem(), dataset.DataItem(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_data_items(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_annotated_dataset(
    transport: str = "grpc",
    request_type=data_labeling_service.GetAnnotatedDatasetRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_annotated_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.AnnotatedDataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            annotation_source=annotation.AnnotationSource.OPERATOR,
            annotation_type=annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION,
            example_count=1396,
            completed_example_count=2448,
            blocking_resources=["blocking_resources_value"],
        )

        response = client.get_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetAnnotatedDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.AnnotatedDataset)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.annotation_source == annotation.AnnotationSource.OPERATOR

    assert (
        response.annotation_type
        == annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION
    )

    assert response.example_count == 1396

    assert response.completed_example_count == 2448

    assert response.blocking_resources == ["blocking_resources_value"]


def test_get_annotated_dataset_from_dict():
    test_get_annotated_dataset(request_type=dict)


@pytest.mark.asyncio
async def test_get_annotated_dataset_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetAnnotatedDatasetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_annotated_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.AnnotatedDataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                annotation_source=annotation.AnnotationSource.OPERATOR,
                annotation_type=annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION,
                example_count=1396,
                completed_example_count=2448,
                blocking_resources=["blocking_resources_value"],
            )
        )

        response = await client.get_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.AnnotatedDataset)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.annotation_source == annotation.AnnotationSource.OPERATOR

    assert (
        response.annotation_type
        == annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION
    )

    assert response.example_count == 1396

    assert response.completed_example_count == 2448

    assert response.blocking_resources == ["blocking_resources_value"]


def test_get_annotated_dataset_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetAnnotatedDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_annotated_dataset), "__call__"
    ) as call:
        call.return_value = dataset.AnnotatedDataset()

        client.get_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_annotated_dataset_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetAnnotatedDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_annotated_dataset), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.AnnotatedDataset()
        )

        await client.get_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_annotated_dataset_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_annotated_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.AnnotatedDataset()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_annotated_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_annotated_dataset_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_annotated_dataset(
            data_labeling_service.GetAnnotatedDatasetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_annotated_dataset_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_annotated_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.AnnotatedDataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.AnnotatedDataset()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_annotated_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_annotated_dataset_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_annotated_dataset(
            data_labeling_service.GetAnnotatedDatasetRequest(), name="name_value",
        )


def test_list_annotated_datasets(
    transport: str = "grpc",
    request_type=data_labeling_service.ListAnnotatedDatasetsRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotated_datasets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListAnnotatedDatasetsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_annotated_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ListAnnotatedDatasetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnnotatedDatasetsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_annotated_datasets_from_dict():
    test_list_annotated_datasets(request_type=dict)


@pytest.mark.asyncio
async def test_list_annotated_datasets_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ListAnnotatedDatasetsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotated_datasets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListAnnotatedDatasetsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_annotated_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnnotatedDatasetsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_annotated_datasets_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListAnnotatedDatasetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotated_datasets), "__call__"
    ) as call:
        call.return_value = data_labeling_service.ListAnnotatedDatasetsResponse()

        client.list_annotated_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_annotated_datasets_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListAnnotatedDatasetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotated_datasets), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListAnnotatedDatasetsResponse()
        )

        await client.list_annotated_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_annotated_datasets_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotated_datasets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListAnnotatedDatasetsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_annotated_datasets(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_annotated_datasets_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_annotated_datasets(
            data_labeling_service.ListAnnotatedDatasetsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_annotated_datasets_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotated_datasets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListAnnotatedDatasetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListAnnotatedDatasetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_annotated_datasets(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_annotated_datasets_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_annotated_datasets(
            data_labeling_service.ListAnnotatedDatasetsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_annotated_datasets_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotated_datasets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[dataset.AnnotatedDataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_annotated_datasets(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dataset.AnnotatedDataset) for i in results)


def test_list_annotated_datasets_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotated_datasets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[dataset.AnnotatedDataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_annotated_datasets(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_annotated_datasets_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotated_datasets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[dataset.AnnotatedDataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_annotated_datasets(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataset.AnnotatedDataset) for i in responses)


@pytest.mark.asyncio
async def test_list_annotated_datasets_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotated_datasets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[dataset.AnnotatedDataset(),], next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotatedDatasetsResponse(
                annotated_datasets=[
                    dataset.AnnotatedDataset(),
                    dataset.AnnotatedDataset(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_annotated_datasets(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_annotated_dataset(
    transport: str = "grpc",
    request_type=data_labeling_service.DeleteAnnotatedDatasetRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_annotated_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.DeleteAnnotatedDatasetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_annotated_dataset_from_dict():
    test_delete_annotated_dataset(request_type=dict)


@pytest.mark.asyncio
async def test_delete_annotated_dataset_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.DeleteAnnotatedDatasetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_annotated_dataset), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_annotated_dataset_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteAnnotatedDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_annotated_dataset), "__call__"
    ) as call:
        call.return_value = None

        client.delete_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_annotated_dataset_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteAnnotatedDatasetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_annotated_dataset), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_annotated_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_label_image(
    transport: str = "grpc", request_type=data_labeling_service.LabelImageRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.label_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.LabelImageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_label_image_from_dict():
    test_label_image(request_type=dict)


@pytest.mark.asyncio
async def test_label_image_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.LabelImageRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_image), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.label_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_label_image_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.LabelImageRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_image), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.label_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_label_image_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.LabelImageRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_image), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.label_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_label_image_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.label_image(
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelImageRequest.Feature.CLASSIFICATION,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].basic_config == human_annotation_config.HumanAnnotationConfig(
            instruction="instruction_value"
        )

        assert (
            args[0].feature
            == data_labeling_service.LabelImageRequest.Feature.CLASSIFICATION
        )


def test_label_image_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.label_image(
            data_labeling_service.LabelImageRequest(),
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelImageRequest.Feature.CLASSIFICATION,
        )


@pytest.mark.asyncio
async def test_label_image_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_image), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.label_image(
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelImageRequest.Feature.CLASSIFICATION,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].basic_config == human_annotation_config.HumanAnnotationConfig(
            instruction="instruction_value"
        )

        assert (
            args[0].feature
            == data_labeling_service.LabelImageRequest.Feature.CLASSIFICATION
        )


@pytest.mark.asyncio
async def test_label_image_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.label_image(
            data_labeling_service.LabelImageRequest(),
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelImageRequest.Feature.CLASSIFICATION,
        )


def test_label_video(
    transport: str = "grpc", request_type=data_labeling_service.LabelVideoRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_video), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.label_video(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.LabelVideoRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_label_video_from_dict():
    test_label_video(request_type=dict)


@pytest.mark.asyncio
async def test_label_video_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.LabelVideoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_video), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.label_video(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_label_video_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.LabelVideoRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_video), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.label_video(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_label_video_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.LabelVideoRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_video), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.label_video(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_label_video_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_video), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.label_video(
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelVideoRequest.Feature.CLASSIFICATION,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].basic_config == human_annotation_config.HumanAnnotationConfig(
            instruction="instruction_value"
        )

        assert (
            args[0].feature
            == data_labeling_service.LabelVideoRequest.Feature.CLASSIFICATION
        )


def test_label_video_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.label_video(
            data_labeling_service.LabelVideoRequest(),
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelVideoRequest.Feature.CLASSIFICATION,
        )


@pytest.mark.asyncio
async def test_label_video_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_video), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.label_video(
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelVideoRequest.Feature.CLASSIFICATION,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].basic_config == human_annotation_config.HumanAnnotationConfig(
            instruction="instruction_value"
        )

        assert (
            args[0].feature
            == data_labeling_service.LabelVideoRequest.Feature.CLASSIFICATION
        )


@pytest.mark.asyncio
async def test_label_video_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.label_video(
            data_labeling_service.LabelVideoRequest(),
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelVideoRequest.Feature.CLASSIFICATION,
        )


def test_label_text(
    transport: str = "grpc", request_type=data_labeling_service.LabelTextRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.label_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.LabelTextRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_label_text_from_dict():
    test_label_text(request_type=dict)


@pytest.mark.asyncio
async def test_label_text_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.LabelTextRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_text), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.label_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_label_text_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.LabelTextRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_text), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.label_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_label_text_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.LabelTextRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_text), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.label_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_label_text_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.label_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.label_text(
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelTextRequest.Feature.TEXT_CLASSIFICATION,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].basic_config == human_annotation_config.HumanAnnotationConfig(
            instruction="instruction_value"
        )

        assert (
            args[0].feature
            == data_labeling_service.LabelTextRequest.Feature.TEXT_CLASSIFICATION
        )


def test_label_text_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.label_text(
            data_labeling_service.LabelTextRequest(),
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelTextRequest.Feature.TEXT_CLASSIFICATION,
        )


@pytest.mark.asyncio
async def test_label_text_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.label_text), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.label_text(
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelTextRequest.Feature.TEXT_CLASSIFICATION,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].basic_config == human_annotation_config.HumanAnnotationConfig(
            instruction="instruction_value"
        )

        assert (
            args[0].feature
            == data_labeling_service.LabelTextRequest.Feature.TEXT_CLASSIFICATION
        )


@pytest.mark.asyncio
async def test_label_text_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.label_text(
            data_labeling_service.LabelTextRequest(),
            parent="parent_value",
            basic_config=human_annotation_config.HumanAnnotationConfig(
                instruction="instruction_value"
            ),
            feature=data_labeling_service.LabelTextRequest.Feature.TEXT_CLASSIFICATION,
        )


def test_get_example(
    transport: str = "grpc", request_type=data_labeling_service.GetExampleRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_example), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Example(
            name="name_value",
            image_payload=data_payloads.ImagePayload(mime_type="mime_type_value"),
        )

        response = client.get_example(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetExampleRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Example)

    assert response.name == "name_value"


def test_get_example_from_dict():
    test_get_example(request_type=dict)


@pytest.mark.asyncio
async def test_get_example_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetExampleRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_example), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.Example(name="name_value",)
        )

        response = await client.get_example(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Example)

    assert response.name == "name_value"


def test_get_example_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetExampleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_example), "__call__") as call:
        call.return_value = dataset.Example()

        client.get_example(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_example_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetExampleRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_example), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Example())

        await client.get_example(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_example_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_example), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Example()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_example(
            name="name_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].filter == "filter_value"


def test_get_example_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_example(
            data_labeling_service.GetExampleRequest(),
            name="name_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_get_example_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_example), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Example()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Example())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_example(name="name_value", filter="filter_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_get_example_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_example(
            data_labeling_service.GetExampleRequest(),
            name="name_value",
            filter="filter_value",
        )


def test_list_examples(
    transport: str = "grpc", request_type=data_labeling_service.ListExamplesRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_examples), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListExamplesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ListExamplesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListExamplesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_examples_from_dict():
    test_list_examples(request_type=dict)


@pytest.mark.asyncio
async def test_list_examples_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ListExamplesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_examples), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListExamplesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListExamplesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_examples_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListExamplesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_examples), "__call__") as call:
        call.return_value = data_labeling_service.ListExamplesResponse()

        client.list_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_examples_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListExamplesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_examples), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListExamplesResponse()
        )

        await client.list_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_examples_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_examples), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListExamplesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_examples(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_examples_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_examples(
            data_labeling_service.ListExamplesRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_examples_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_examples), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListExamplesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListExamplesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_examples(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_examples_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_examples(
            data_labeling_service.ListExamplesRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_examples_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_examples), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(), dataset.Example(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[], next_page_token="def",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(),], next_page_token="ghi",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_examples(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dataset.Example) for i in results)


def test_list_examples_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_examples), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(), dataset.Example(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[], next_page_token="def",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(),], next_page_token="ghi",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_examples(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_examples_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_examples),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(), dataset.Example(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[], next_page_token="def",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(),], next_page_token="ghi",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_examples(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataset.Example) for i in responses)


@pytest.mark.asyncio
async def test_list_examples_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_examples),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(), dataset.Example(),],
                next_page_token="abc",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[], next_page_token="def",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(),], next_page_token="ghi",
            ),
            data_labeling_service.ListExamplesResponse(
                examples=[dataset.Example(), dataset.Example(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_examples(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_create_annotation_spec_set(
    transport: str = "grpc",
    request_type=data_labeling_service.CreateAnnotationSpecSetRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_annotation_spec_set.AnnotationSpecSet(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            blocking_resources=["blocking_resources_value"],
        )

        response = client.create_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.CreateAnnotationSpecSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_annotation_spec_set.AnnotationSpecSet)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]


def test_create_annotation_spec_set_from_dict():
    test_create_annotation_spec_set(request_type=dict)


@pytest.mark.asyncio
async def test_create_annotation_spec_set_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.CreateAnnotationSpecSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_annotation_spec_set.AnnotationSpecSet(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                blocking_resources=["blocking_resources_value"],
            )
        )

        response = await client.create_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_annotation_spec_set.AnnotationSpecSet)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]


def test_create_annotation_spec_set_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateAnnotationSpecSetRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_annotation_spec_set), "__call__"
    ) as call:
        call.return_value = gcd_annotation_spec_set.AnnotationSpecSet()

        client.create_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_annotation_spec_set_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateAnnotationSpecSetRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_annotation_spec_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_annotation_spec_set.AnnotationSpecSet()
        )

        await client.create_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_annotation_spec_set_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_annotation_spec_set.AnnotationSpecSet()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_annotation_spec_set(
            parent="parent_value",
            annotation_spec_set=gcd_annotation_spec_set.AnnotationSpecSet(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].annotation_spec_set == gcd_annotation_spec_set.AnnotationSpecSet(
            name="name_value"
        )


def test_create_annotation_spec_set_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_annotation_spec_set(
            data_labeling_service.CreateAnnotationSpecSetRequest(),
            parent="parent_value",
            annotation_spec_set=gcd_annotation_spec_set.AnnotationSpecSet(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_annotation_spec_set_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_annotation_spec_set.AnnotationSpecSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_annotation_spec_set.AnnotationSpecSet()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_annotation_spec_set(
            parent="parent_value",
            annotation_spec_set=gcd_annotation_spec_set.AnnotationSpecSet(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].annotation_spec_set == gcd_annotation_spec_set.AnnotationSpecSet(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_annotation_spec_set_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_annotation_spec_set(
            data_labeling_service.CreateAnnotationSpecSetRequest(),
            parent="parent_value",
            annotation_spec_set=gcd_annotation_spec_set.AnnotationSpecSet(
                name="name_value"
            ),
        )


def test_get_annotation_spec_set(
    transport: str = "grpc",
    request_type=data_labeling_service.GetAnnotationSpecSetRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = annotation_spec_set.AnnotationSpecSet(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            blocking_resources=["blocking_resources_value"],
        )

        response = client.get_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetAnnotationSpecSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, annotation_spec_set.AnnotationSpecSet)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]


def test_get_annotation_spec_set_from_dict():
    test_get_annotation_spec_set(request_type=dict)


@pytest.mark.asyncio
async def test_get_annotation_spec_set_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetAnnotationSpecSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            annotation_spec_set.AnnotationSpecSet(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                blocking_resources=["blocking_resources_value"],
            )
        )

        response = await client.get_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, annotation_spec_set.AnnotationSpecSet)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.blocking_resources == ["blocking_resources_value"]


def test_get_annotation_spec_set_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetAnnotationSpecSetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_annotation_spec_set), "__call__"
    ) as call:
        call.return_value = annotation_spec_set.AnnotationSpecSet()

        client.get_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_annotation_spec_set_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetAnnotationSpecSetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_annotation_spec_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            annotation_spec_set.AnnotationSpecSet()
        )

        await client.get_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_annotation_spec_set_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = annotation_spec_set.AnnotationSpecSet()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_annotation_spec_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_annotation_spec_set_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_annotation_spec_set(
            data_labeling_service.GetAnnotationSpecSetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_annotation_spec_set_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = annotation_spec_set.AnnotationSpecSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            annotation_spec_set.AnnotationSpecSet()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_annotation_spec_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_annotation_spec_set_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_annotation_spec_set(
            data_labeling_service.GetAnnotationSpecSetRequest(), name="name_value",
        )


def test_list_annotation_spec_sets(
    transport: str = "grpc",
    request_type=data_labeling_service.ListAnnotationSpecSetsRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListAnnotationSpecSetsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_annotation_spec_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ListAnnotationSpecSetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnnotationSpecSetsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_annotation_spec_sets_from_dict():
    test_list_annotation_spec_sets(request_type=dict)


@pytest.mark.asyncio
async def test_list_annotation_spec_sets_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ListAnnotationSpecSetsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListAnnotationSpecSetsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_annotation_spec_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnnotationSpecSetsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_annotation_spec_sets_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListAnnotationSpecSetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        call.return_value = data_labeling_service.ListAnnotationSpecSetsResponse()

        client.list_annotation_spec_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_annotation_spec_sets_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListAnnotationSpecSetsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListAnnotationSpecSetsResponse()
        )

        await client.list_annotation_spec_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_annotation_spec_sets_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListAnnotationSpecSetsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_annotation_spec_sets(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_annotation_spec_sets_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_annotation_spec_sets(
            data_labeling_service.ListAnnotationSpecSetsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_annotation_spec_sets_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListAnnotationSpecSetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListAnnotationSpecSetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_annotation_spec_sets(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_annotation_spec_sets_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_annotation_spec_sets(
            data_labeling_service.ListAnnotationSpecSetsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_annotation_spec_sets_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[annotation_spec_set.AnnotationSpecSet(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_annotation_spec_sets(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, annotation_spec_set.AnnotationSpecSet) for i in results
        )


def test_list_annotation_spec_sets_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_annotation_spec_sets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[annotation_spec_set.AnnotationSpecSet(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_annotation_spec_sets(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_annotation_spec_sets_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotation_spec_sets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[annotation_spec_set.AnnotationSpecSet(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_annotation_spec_sets(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, annotation_spec_set.AnnotationSpecSet) for i in responses
        )


@pytest.mark.asyncio
async def test_list_annotation_spec_sets_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_annotation_spec_sets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[], next_page_token="def",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[annotation_spec_set.AnnotationSpecSet(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListAnnotationSpecSetsResponse(
                annotation_spec_sets=[
                    annotation_spec_set.AnnotationSpecSet(),
                    annotation_spec_set.AnnotationSpecSet(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_annotation_spec_sets(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_annotation_spec_set(
    transport: str = "grpc",
    request_type=data_labeling_service.DeleteAnnotationSpecSetRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.DeleteAnnotationSpecSetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_annotation_spec_set_from_dict():
    test_delete_annotation_spec_set(request_type=dict)


@pytest.mark.asyncio
async def test_delete_annotation_spec_set_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.DeleteAnnotationSpecSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_annotation_spec_set_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteAnnotationSpecSetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_annotation_spec_set), "__call__"
    ) as call:
        call.return_value = None

        client.delete_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_annotation_spec_set_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteAnnotationSpecSetRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_annotation_spec_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_annotation_spec_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_annotation_spec_set_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_annotation_spec_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_annotation_spec_set_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_annotation_spec_set(
            data_labeling_service.DeleteAnnotationSpecSetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_annotation_spec_set_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_annotation_spec_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_annotation_spec_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_annotation_spec_set_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_annotation_spec_set(
            data_labeling_service.DeleteAnnotationSpecSetRequest(), name="name_value",
        )


def test_create_instruction(
    transport: str = "grpc", request_type=data_labeling_service.CreateInstructionRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.create_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.CreateInstructionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_instruction_from_dict():
    test_create_instruction(request_type=dict)


@pytest.mark.asyncio
async def test_create_instruction_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.CreateInstructionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.create_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_instruction_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateInstructionRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_instruction), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.create_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_instruction_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateInstructionRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_instruction), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.create_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_instruction_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_instruction(
            parent="parent_value",
            instruction=gcd_instruction.Instruction(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].instruction == gcd_instruction.Instruction(name="name_value")


def test_create_instruction_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_instruction(
            data_labeling_service.CreateInstructionRequest(),
            parent="parent_value",
            instruction=gcd_instruction.Instruction(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_instruction_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_instruction(
            parent="parent_value",
            instruction=gcd_instruction.Instruction(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].instruction == gcd_instruction.Instruction(name="name_value")


@pytest.mark.asyncio
async def test_create_instruction_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_instruction(
            data_labeling_service.CreateInstructionRequest(),
            parent="parent_value",
            instruction=gcd_instruction.Instruction(name="name_value"),
        )


def test_get_instruction(
    transport: str = "grpc", request_type=data_labeling_service.GetInstructionRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_instruction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instruction.Instruction(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            data_type=dataset.DataType.IMAGE,
            blocking_resources=["blocking_resources_value"],
        )

        response = client.get_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetInstructionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, instruction.Instruction)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.data_type == dataset.DataType.IMAGE

    assert response.blocking_resources == ["blocking_resources_value"]


def test_get_instruction_from_dict():
    test_get_instruction(request_type=dict)


@pytest.mark.asyncio
async def test_get_instruction_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetInstructionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instruction.Instruction(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                data_type=dataset.DataType.IMAGE,
                blocking_resources=["blocking_resources_value"],
            )
        )

        response = await client.get_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, instruction.Instruction)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.data_type == dataset.DataType.IMAGE

    assert response.blocking_resources == ["blocking_resources_value"]


def test_get_instruction_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetInstructionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_instruction), "__call__") as call:
        call.return_value = instruction.Instruction()

        client.get_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_instruction_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetInstructionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_instruction), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instruction.Instruction()
        )

        await client.get_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_instruction_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_instruction), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instruction.Instruction()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_instruction(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_instruction_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_instruction(
            data_labeling_service.GetInstructionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_instruction_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = instruction.Instruction()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instruction.Instruction()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_instruction(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_instruction_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_instruction(
            data_labeling_service.GetInstructionRequest(), name="name_value",
        )


def test_list_instructions(
    transport: str = "grpc", request_type=data_labeling_service.ListInstructionsRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_instructions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListInstructionsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_instructions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ListInstructionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstructionsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_instructions_from_dict():
    test_list_instructions(request_type=dict)


@pytest.mark.asyncio
async def test_list_instructions_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ListInstructionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_instructions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListInstructionsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_instructions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstructionsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_instructions_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListInstructionsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_instructions), "__call__"
    ) as call:
        call.return_value = data_labeling_service.ListInstructionsResponse()

        client.list_instructions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_instructions_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListInstructionsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_instructions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListInstructionsResponse()
        )

        await client.list_instructions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_instructions_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_instructions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListInstructionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_instructions(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_instructions_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_instructions(
            data_labeling_service.ListInstructionsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_instructions_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_instructions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListInstructionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListInstructionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_instructions(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_instructions_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_instructions(
            data_labeling_service.ListInstructionsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_instructions_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_instructions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListInstructionsResponse(
                instructions=[
                    instruction.Instruction(),
                    instruction.Instruction(),
                    instruction.Instruction(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[], next_page_token="def",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(),], next_page_token="ghi",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(), instruction.Instruction(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_instructions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, instruction.Instruction) for i in results)


def test_list_instructions_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_instructions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListInstructionsResponse(
                instructions=[
                    instruction.Instruction(),
                    instruction.Instruction(),
                    instruction.Instruction(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[], next_page_token="def",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(),], next_page_token="ghi",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(), instruction.Instruction(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_instructions(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_instructions_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_instructions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListInstructionsResponse(
                instructions=[
                    instruction.Instruction(),
                    instruction.Instruction(),
                    instruction.Instruction(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[], next_page_token="def",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(),], next_page_token="ghi",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(), instruction.Instruction(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_instructions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, instruction.Instruction) for i in responses)


@pytest.mark.asyncio
async def test_list_instructions_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_instructions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListInstructionsResponse(
                instructions=[
                    instruction.Instruction(),
                    instruction.Instruction(),
                    instruction.Instruction(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[], next_page_token="def",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(),], next_page_token="ghi",
            ),
            data_labeling_service.ListInstructionsResponse(
                instructions=[instruction.Instruction(), instruction.Instruction(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_instructions(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_instruction(
    transport: str = "grpc", request_type=data_labeling_service.DeleteInstructionRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.DeleteInstructionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_instruction_from_dict():
    test_delete_instruction(request_type=dict)


@pytest.mark.asyncio
async def test_delete_instruction_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.DeleteInstructionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_instruction_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteInstructionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_instruction), "__call__"
    ) as call:
        call.return_value = None

        client.delete_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_instruction_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteInstructionRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_instruction), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_instruction(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_instruction_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_instruction(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_instruction_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_instruction(
            data_labeling_service.DeleteInstructionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_instruction_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_instruction), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_instruction(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_instruction_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_instruction(
            data_labeling_service.DeleteInstructionRequest(), name="name_value",
        )


def test_get_evaluation(
    transport: str = "grpc", request_type=data_labeling_service.GetEvaluationRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_evaluation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation.Evaluation(
            name="name_value",
            annotation_type=annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION,
            evaluated_item_count=2129,
        )

        response = client.get_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetEvaluationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, evaluation.Evaluation)

    assert response.name == "name_value"

    assert (
        response.annotation_type
        == annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION
    )

    assert response.evaluated_item_count == 2129


def test_get_evaluation_from_dict():
    test_get_evaluation(request_type=dict)


@pytest.mark.asyncio
async def test_get_evaluation_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetEvaluationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_evaluation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation.Evaluation(
                name="name_value",
                annotation_type=annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION,
                evaluated_item_count=2129,
            )
        )

        response = await client.get_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, evaluation.Evaluation)

    assert response.name == "name_value"

    assert (
        response.annotation_type
        == annotation.AnnotationType.IMAGE_CLASSIFICATION_ANNOTATION
    )

    assert response.evaluated_item_count == 2129


def test_get_evaluation_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetEvaluationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_evaluation), "__call__") as call:
        call.return_value = evaluation.Evaluation()

        client.get_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_evaluation_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetEvaluationRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_evaluation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation.Evaluation()
        )

        await client.get_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_evaluation_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_evaluation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation.Evaluation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_evaluation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_evaluation_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_evaluation(
            data_labeling_service.GetEvaluationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_evaluation_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_evaluation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation.Evaluation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation.Evaluation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_evaluation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_evaluation_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_evaluation(
            data_labeling_service.GetEvaluationRequest(), name="name_value",
        )


def test_search_evaluations(
    transport: str = "grpc", request_type=data_labeling_service.SearchEvaluationsRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.SearchEvaluationsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.search_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.SearchEvaluationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchEvaluationsPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_evaluations_from_dict():
    test_search_evaluations(request_type=dict)


@pytest.mark.asyncio
async def test_search_evaluations_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.SearchEvaluationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.SearchEvaluationsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.search_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchEvaluationsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_evaluations_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.SearchEvaluationsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_evaluations), "__call__"
    ) as call:
        call.return_value = data_labeling_service.SearchEvaluationsResponse()

        client.search_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_evaluations_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.SearchEvaluationsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_evaluations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.SearchEvaluationsResponse()
        )

        await client.search_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_search_evaluations_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.SearchEvaluationsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_evaluations(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_search_evaluations_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_evaluations(
            data_labeling_service.SearchEvaluationsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_search_evaluations_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.SearchEvaluationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.SearchEvaluationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_evaluations(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_search_evaluations_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_evaluations(
            data_labeling_service.SearchEvaluationsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_search_evaluations_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_evaluations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[], next_page_token="def",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(),], next_page_token="ghi",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(), evaluation.Evaluation(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.search_evaluations(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, evaluation.Evaluation) for i in results)


def test_search_evaluations_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_evaluations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[], next_page_token="def",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(),], next_page_token="ghi",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(), evaluation.Evaluation(),],
            ),
            RuntimeError,
        )
        pages = list(client.search_evaluations(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_evaluations_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_evaluations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[], next_page_token="def",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(),], next_page_token="ghi",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(), evaluation.Evaluation(),],
            ),
            RuntimeError,
        )
        async_pager = await client.search_evaluations(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, evaluation.Evaluation) for i in responses)


@pytest.mark.asyncio
async def test_search_evaluations_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_evaluations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                    evaluation.Evaluation(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[], next_page_token="def",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(),], next_page_token="ghi",
            ),
            data_labeling_service.SearchEvaluationsResponse(
                evaluations=[evaluation.Evaluation(), evaluation.Evaluation(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.search_evaluations(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_search_example_comparisons(
    transport: str = "grpc",
    request_type=data_labeling_service.SearchExampleComparisonsRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_example_comparisons), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.SearchExampleComparisonsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.search_example_comparisons(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.SearchExampleComparisonsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchExampleComparisonsPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_example_comparisons_from_dict():
    test_search_example_comparisons(request_type=dict)


@pytest.mark.asyncio
async def test_search_example_comparisons_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.SearchExampleComparisonsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_example_comparisons), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.SearchExampleComparisonsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.search_example_comparisons(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchExampleComparisonsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_example_comparisons_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.SearchExampleComparisonsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_example_comparisons), "__call__"
    ) as call:
        call.return_value = data_labeling_service.SearchExampleComparisonsResponse()

        client.search_example_comparisons(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_example_comparisons_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.SearchExampleComparisonsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_example_comparisons), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.SearchExampleComparisonsResponse()
        )

        await client.search_example_comparisons(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_search_example_comparisons_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_example_comparisons), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.SearchExampleComparisonsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_example_comparisons(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_search_example_comparisons_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_example_comparisons(
            data_labeling_service.SearchExampleComparisonsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_search_example_comparisons_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_example_comparisons), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.SearchExampleComparisonsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.SearchExampleComparisonsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_example_comparisons(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_search_example_comparisons_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_example_comparisons(
            data_labeling_service.SearchExampleComparisonsRequest(),
            parent="parent_value",
        )


def test_search_example_comparisons_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_example_comparisons), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[], next_page_token="def",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="ghi",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.search_example_comparisons(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(
                i,
                data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison,
            )
            for i in results
        )


def test_search_example_comparisons_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.search_example_comparisons), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[], next_page_token="def",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="ghi",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_example_comparisons(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_example_comparisons_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_example_comparisons),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[], next_page_token="def",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="ghi",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_example_comparisons(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(
                i,
                data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison,
            )
            for i in responses
        )


@pytest.mark.asyncio
async def test_search_example_comparisons_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_example_comparisons),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[], next_page_token="def",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
                next_page_token="ghi",
            ),
            data_labeling_service.SearchExampleComparisonsResponse(
                example_comparisons=[
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                    data_labeling_service.SearchExampleComparisonsResponse.ExampleComparison(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.search_example_comparisons(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_create_evaluation_job(
    transport: str = "grpc",
    request_type=data_labeling_service.CreateEvaluationJobRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation_job.EvaluationJob(
            name="name_value",
            description="description_value",
            state=evaluation_job.EvaluationJob.State.SCHEDULED,
            schedule="schedule_value",
            model_version="model_version_value",
            annotation_spec_set="annotation_spec_set_value",
            label_missing_ground_truth=True,
        )

        response = client.create_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.CreateEvaluationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, evaluation_job.EvaluationJob)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == evaluation_job.EvaluationJob.State.SCHEDULED

    assert response.schedule == "schedule_value"

    assert response.model_version == "model_version_value"

    assert response.annotation_spec_set == "annotation_spec_set_value"

    assert response.label_missing_ground_truth is True


def test_create_evaluation_job_from_dict():
    test_create_evaluation_job(request_type=dict)


@pytest.mark.asyncio
async def test_create_evaluation_job_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.CreateEvaluationJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation_job.EvaluationJob(
                name="name_value",
                description="description_value",
                state=evaluation_job.EvaluationJob.State.SCHEDULED,
                schedule="schedule_value",
                model_version="model_version_value",
                annotation_spec_set="annotation_spec_set_value",
                label_missing_ground_truth=True,
            )
        )

        response = await client.create_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, evaluation_job.EvaluationJob)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == evaluation_job.EvaluationJob.State.SCHEDULED

    assert response.schedule == "schedule_value"

    assert response.model_version == "model_version_value"

    assert response.annotation_spec_set == "annotation_spec_set_value"

    assert response.label_missing_ground_truth is True


def test_create_evaluation_job_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateEvaluationJobRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_evaluation_job), "__call__"
    ) as call:
        call.return_value = evaluation_job.EvaluationJob()

        client.create_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_evaluation_job_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.CreateEvaluationJobRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_evaluation_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation_job.EvaluationJob()
        )

        await client.create_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_evaluation_job_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation_job.EvaluationJob()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_evaluation_job(
            parent="parent_value", job=evaluation_job.EvaluationJob(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].job == evaluation_job.EvaluationJob(name="name_value")


def test_create_evaluation_job_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_evaluation_job(
            data_labeling_service.CreateEvaluationJobRequest(),
            parent="parent_value",
            job=evaluation_job.EvaluationJob(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_evaluation_job_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation_job.EvaluationJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation_job.EvaluationJob()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_evaluation_job(
            parent="parent_value", job=evaluation_job.EvaluationJob(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].job == evaluation_job.EvaluationJob(name="name_value")


@pytest.mark.asyncio
async def test_create_evaluation_job_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_evaluation_job(
            data_labeling_service.CreateEvaluationJobRequest(),
            parent="parent_value",
            job=evaluation_job.EvaluationJob(name="name_value"),
        )


def test_update_evaluation_job(
    transport: str = "grpc",
    request_type=data_labeling_service.UpdateEvaluationJobRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_evaluation_job.EvaluationJob(
            name="name_value",
            description="description_value",
            state=gcd_evaluation_job.EvaluationJob.State.SCHEDULED,
            schedule="schedule_value",
            model_version="model_version_value",
            annotation_spec_set="annotation_spec_set_value",
            label_missing_ground_truth=True,
        )

        response = client.update_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.UpdateEvaluationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_evaluation_job.EvaluationJob)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == gcd_evaluation_job.EvaluationJob.State.SCHEDULED

    assert response.schedule == "schedule_value"

    assert response.model_version == "model_version_value"

    assert response.annotation_spec_set == "annotation_spec_set_value"

    assert response.label_missing_ground_truth is True


def test_update_evaluation_job_from_dict():
    test_update_evaluation_job(request_type=dict)


@pytest.mark.asyncio
async def test_update_evaluation_job_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.UpdateEvaluationJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_evaluation_job.EvaluationJob(
                name="name_value",
                description="description_value",
                state=gcd_evaluation_job.EvaluationJob.State.SCHEDULED,
                schedule="schedule_value",
                model_version="model_version_value",
                annotation_spec_set="annotation_spec_set_value",
                label_missing_ground_truth=True,
            )
        )

        response = await client.update_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_evaluation_job.EvaluationJob)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == gcd_evaluation_job.EvaluationJob.State.SCHEDULED

    assert response.schedule == "schedule_value"

    assert response.model_version == "model_version_value"

    assert response.annotation_spec_set == "annotation_spec_set_value"

    assert response.label_missing_ground_truth is True


def test_update_evaluation_job_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.UpdateEvaluationJobRequest()
    request.evaluation_job.name = "evaluation_job.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_evaluation_job), "__call__"
    ) as call:
        call.return_value = gcd_evaluation_job.EvaluationJob()

        client.update_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "evaluation_job.name=evaluation_job.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_evaluation_job_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.UpdateEvaluationJobRequest()
    request.evaluation_job.name = "evaluation_job.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_evaluation_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_evaluation_job.EvaluationJob()
        )

        await client.update_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "evaluation_job.name=evaluation_job.name/value",
    ) in kw["metadata"]


def test_update_evaluation_job_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_evaluation_job.EvaluationJob()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_evaluation_job(
            evaluation_job=gcd_evaluation_job.EvaluationJob(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].evaluation_job == gcd_evaluation_job.EvaluationJob(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_evaluation_job_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_evaluation_job(
            data_labeling_service.UpdateEvaluationJobRequest(),
            evaluation_job=gcd_evaluation_job.EvaluationJob(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_evaluation_job_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_evaluation_job.EvaluationJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_evaluation_job.EvaluationJob()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_evaluation_job(
            evaluation_job=gcd_evaluation_job.EvaluationJob(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].evaluation_job == gcd_evaluation_job.EvaluationJob(
            name="name_value"
        )

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_evaluation_job_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_evaluation_job(
            data_labeling_service.UpdateEvaluationJobRequest(),
            evaluation_job=gcd_evaluation_job.EvaluationJob(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_get_evaluation_job(
    transport: str = "grpc", request_type=data_labeling_service.GetEvaluationJobRequest
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation_job.EvaluationJob(
            name="name_value",
            description="description_value",
            state=evaluation_job.EvaluationJob.State.SCHEDULED,
            schedule="schedule_value",
            model_version="model_version_value",
            annotation_spec_set="annotation_spec_set_value",
            label_missing_ground_truth=True,
        )

        response = client.get_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.GetEvaluationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, evaluation_job.EvaluationJob)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == evaluation_job.EvaluationJob.State.SCHEDULED

    assert response.schedule == "schedule_value"

    assert response.model_version == "model_version_value"

    assert response.annotation_spec_set == "annotation_spec_set_value"

    assert response.label_missing_ground_truth is True


def test_get_evaluation_job_from_dict():
    test_get_evaluation_job(request_type=dict)


@pytest.mark.asyncio
async def test_get_evaluation_job_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.GetEvaluationJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation_job.EvaluationJob(
                name="name_value",
                description="description_value",
                state=evaluation_job.EvaluationJob.State.SCHEDULED,
                schedule="schedule_value",
                model_version="model_version_value",
                annotation_spec_set="annotation_spec_set_value",
                label_missing_ground_truth=True,
            )
        )

        response = await client.get_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, evaluation_job.EvaluationJob)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.state == evaluation_job.EvaluationJob.State.SCHEDULED

    assert response.schedule == "schedule_value"

    assert response.model_version == "model_version_value"

    assert response.annotation_spec_set == "annotation_spec_set_value"

    assert response.label_missing_ground_truth is True


def test_get_evaluation_job_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_evaluation_job), "__call__"
    ) as call:
        call.return_value = evaluation_job.EvaluationJob()

        client.get_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_evaluation_job_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.GetEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_evaluation_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation_job.EvaluationJob()
        )

        await client.get_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_evaluation_job_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation_job.EvaluationJob()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_evaluation_job_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_evaluation_job(
            data_labeling_service.GetEvaluationJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_evaluation_job_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = evaluation_job.EvaluationJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            evaluation_job.EvaluationJob()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_evaluation_job_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_evaluation_job(
            data_labeling_service.GetEvaluationJobRequest(), name="name_value",
        )


def test_pause_evaluation_job(
    transport: str = "grpc",
    request_type=data_labeling_service.PauseEvaluationJobRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.pause_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.pause_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.PauseEvaluationJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_pause_evaluation_job_from_dict():
    test_pause_evaluation_job(request_type=dict)


@pytest.mark.asyncio
async def test_pause_evaluation_job_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.PauseEvaluationJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.pause_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.pause_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_pause_evaluation_job_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.PauseEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.pause_evaluation_job), "__call__"
    ) as call:
        call.return_value = None

        client.pause_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_pause_evaluation_job_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.PauseEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.pause_evaluation_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.pause_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_pause_evaluation_job_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.pause_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.pause_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_pause_evaluation_job_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.pause_evaluation_job(
            data_labeling_service.PauseEvaluationJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_pause_evaluation_job_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.pause_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.pause_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_pause_evaluation_job_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.pause_evaluation_job(
            data_labeling_service.PauseEvaluationJobRequest(), name="name_value",
        )


def test_resume_evaluation_job(
    transport: str = "grpc",
    request_type=data_labeling_service.ResumeEvaluationJobRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.resume_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.resume_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ResumeEvaluationJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_resume_evaluation_job_from_dict():
    test_resume_evaluation_job(request_type=dict)


@pytest.mark.asyncio
async def test_resume_evaluation_job_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ResumeEvaluationJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.resume_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.resume_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_resume_evaluation_job_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ResumeEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.resume_evaluation_job), "__call__"
    ) as call:
        call.return_value = None

        client.resume_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_resume_evaluation_job_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ResumeEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.resume_evaluation_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.resume_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_resume_evaluation_job_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.resume_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.resume_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_resume_evaluation_job_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resume_evaluation_job(
            data_labeling_service.ResumeEvaluationJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_resume_evaluation_job_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.resume_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.resume_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_resume_evaluation_job_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.resume_evaluation_job(
            data_labeling_service.ResumeEvaluationJobRequest(), name="name_value",
        )


def test_delete_evaluation_job(
    transport: str = "grpc",
    request_type=data_labeling_service.DeleteEvaluationJobRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.DeleteEvaluationJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_evaluation_job_from_dict():
    test_delete_evaluation_job(request_type=dict)


@pytest.mark.asyncio
async def test_delete_evaluation_job_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.DeleteEvaluationJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_evaluation_job_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_evaluation_job), "__call__"
    ) as call:
        call.return_value = None

        client.delete_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_evaluation_job_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.DeleteEvaluationJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_evaluation_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_evaluation_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_evaluation_job_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_evaluation_job_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_evaluation_job(
            data_labeling_service.DeleteEvaluationJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_evaluation_job_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_evaluation_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_evaluation_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_evaluation_job_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_evaluation_job(
            data_labeling_service.DeleteEvaluationJobRequest(), name="name_value",
        )


def test_list_evaluation_jobs(
    transport: str = "grpc",
    request_type=data_labeling_service.ListEvaluationJobsRequest,
):
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListEvaluationJobsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_evaluation_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == data_labeling_service.ListEvaluationJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEvaluationJobsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_evaluation_jobs_from_dict():
    test_list_evaluation_jobs(request_type=dict)


@pytest.mark.asyncio
async def test_list_evaluation_jobs_async(transport: str = "grpc_asyncio"):
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = data_labeling_service.ListEvaluationJobsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListEvaluationJobsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_evaluation_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEvaluationJobsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_evaluation_jobs_field_headers():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListEvaluationJobsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        call.return_value = data_labeling_service.ListEvaluationJobsResponse()

        client.list_evaluation_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_evaluation_jobs_field_headers_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = data_labeling_service.ListEvaluationJobsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListEvaluationJobsResponse()
        )

        await client.list_evaluation_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_evaluation_jobs_flattened():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListEvaluationJobsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_evaluation_jobs(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_evaluation_jobs_flattened_error():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_evaluation_jobs(
            data_labeling_service.ListEvaluationJobsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_evaluation_jobs_flattened_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = data_labeling_service.ListEvaluationJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            data_labeling_service.ListEvaluationJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_evaluation_jobs(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_evaluation_jobs_flattened_error_async():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_evaluation_jobs(
            data_labeling_service.ListEvaluationJobsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_evaluation_jobs_pager():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[], next_page_token="def",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[evaluation_job.EvaluationJob(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_evaluation_jobs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, evaluation_job.EvaluationJob) for i in results)


def test_list_evaluation_jobs_pages():
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_evaluation_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[], next_page_token="def",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[evaluation_job.EvaluationJob(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_evaluation_jobs(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_evaluation_jobs_async_pager():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_evaluation_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[], next_page_token="def",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[evaluation_job.EvaluationJob(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_evaluation_jobs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, evaluation_job.EvaluationJob) for i in responses)


@pytest.mark.asyncio
async def test_list_evaluation_jobs_async_pages():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_evaluation_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
                next_page_token="abc",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[], next_page_token="def",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[evaluation_job.EvaluationJob(),],
                next_page_token="ghi",
            ),
            data_labeling_service.ListEvaluationJobsResponse(
                evaluation_jobs=[
                    evaluation_job.EvaluationJob(),
                    evaluation_job.EvaluationJob(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_evaluation_jobs(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataLabelingServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataLabelingServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataLabelingServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataLabelingServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataLabelingServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataLabelingServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataLabelingServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = DataLabelingServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataLabelingServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataLabelingServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DataLabelingServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.DataLabelingServiceGrpcTransport,)


def test_data_labeling_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.DataLabelingServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_data_labeling_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.datalabeling_v1beta1.services.data_labeling_service.transports.DataLabelingServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataLabelingServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_dataset",
        "get_dataset",
        "list_datasets",
        "delete_dataset",
        "import_data",
        "export_data",
        "get_data_item",
        "list_data_items",
        "get_annotated_dataset",
        "list_annotated_datasets",
        "delete_annotated_dataset",
        "label_image",
        "label_video",
        "label_text",
        "get_example",
        "list_examples",
        "create_annotation_spec_set",
        "get_annotation_spec_set",
        "list_annotation_spec_sets",
        "delete_annotation_spec_set",
        "create_instruction",
        "get_instruction",
        "list_instructions",
        "delete_instruction",
        "get_evaluation",
        "search_evaluations",
        "search_example_comparisons",
        "create_evaluation_job",
        "update_evaluation_job",
        "get_evaluation_job",
        "pause_evaluation_job",
        "resume_evaluation_job",
        "delete_evaluation_job",
        "list_evaluation_jobs",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_data_labeling_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.datalabeling_v1beta1.services.data_labeling_service.transports.DataLabelingServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.DataLabelingServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_data_labeling_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        DataLabelingServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_data_labeling_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.DataLabelingServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_data_labeling_service_host_no_port():
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datalabeling.googleapis.com"
        ),
    )
    assert client._transport._host == "datalabeling.googleapis.com:443"


def test_data_labeling_service_host_with_port():
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datalabeling.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "datalabeling.googleapis.com:8000"


def test_data_labeling_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.DataLabelingServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_data_labeling_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.DataLabelingServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_data_labeling_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.DataLabelingServiceGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_data_labeling_service_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.DataLabelingServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_data_labeling_service_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.DataLabelingServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_data_labeling_service_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.DataLabelingServiceGrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_data_labeling_service_grpc_lro_client():
    client = DataLabelingServiceClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_data_labeling_service_grpc_lro_async_client():
    client = DataLabelingServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client._client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_instruction_path():
    project = "squid"
    instruction = "clam"

    expected = "projects/{project}/instructions/{instruction}".format(
        project=project, instruction=instruction,
    )
    actual = DataLabelingServiceClient.instruction_path(project, instruction)
    assert expected == actual


def test_parse_instruction_path():
    expected = {
        "project": "whelk",
        "instruction": "octopus",
    }
    path = DataLabelingServiceClient.instruction_path(**expected)

    # Check that the path construction is reversible.
    actual = DataLabelingServiceClient.parse_instruction_path(path)
    assert expected == actual


def test_annotation_spec_set_path():
    project = "squid"
    annotation_spec_set = "clam"

    expected = "projects/{project}/annotationSpecSets/{annotation_spec_set}".format(
        project=project, annotation_spec_set=annotation_spec_set,
    )
    actual = DataLabelingServiceClient.annotation_spec_set_path(
        project, annotation_spec_set
    )
    assert expected == actual


def test_parse_annotation_spec_set_path():
    expected = {
        "project": "whelk",
        "annotation_spec_set": "octopus",
    }
    path = DataLabelingServiceClient.annotation_spec_set_path(**expected)

    # Check that the path construction is reversible.
    actual = DataLabelingServiceClient.parse_annotation_spec_set_path(path)
    assert expected == actual


def test_evaluation_job_path():
    project = "squid"
    evaluation_job = "clam"

    expected = "projects/{project}/evaluationJobs/{evaluation_job}".format(
        project=project, evaluation_job=evaluation_job,
    )
    actual = DataLabelingServiceClient.evaluation_job_path(project, evaluation_job)
    assert expected == actual


def test_parse_evaluation_job_path():
    expected = {
        "project": "whelk",
        "evaluation_job": "octopus",
    }
    path = DataLabelingServiceClient.evaluation_job_path(**expected)

    # Check that the path construction is reversible.
    actual = DataLabelingServiceClient.parse_evaluation_job_path(path)
    assert expected == actual


def test_dataset_path():
    project = "squid"
    dataset = "clam"

    expected = "projects/{project}/datasets/{dataset}".format(
        project=project, dataset=dataset,
    )
    actual = DataLabelingServiceClient.dataset_path(project, dataset)
    assert expected == actual


def test_parse_dataset_path():
    expected = {
        "project": "whelk",
        "dataset": "octopus",
    }
    path = DataLabelingServiceClient.dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = DataLabelingServiceClient.parse_dataset_path(path)
    assert expected == actual
