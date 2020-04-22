# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import backoff
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import DeadlineExceeded
from google.cloud import datalabeling_v1beta1 as datalabeling

import create_annotation_spec_set as annotation_spec_set_sample
import create_instruction as instruction_sample
import manage_dataset as dataset_sample
import import_data as import_sample

RETRY_DEADLINE = 60


def create_client():
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if 'DATALABELING_ENDPOINT' in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv('DATALABELING_ENDPOINT'))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    else:
        client = datalabeling.DataLabelingServiceClient()
    return client


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def create_dataset(project_id):
    return dataset_sample.create_dataset(project_id)


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def delete_dataset(name):
    return dataset_sample.delete_dataset(name)


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def create_annotation_spec_set(project_id):
    return annotation_spec_set_sample.create_annotation_spec_set(project_id)


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def delete_annotation_spec_set(name):
    client = create_client()
    client.delete_annotation_spec_set(name)


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def create_instruction(project_id, data_type, gcs_uri):
    return instruction_sample.create_instruction(project_id, data_type, gcs_uri)


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def delete_instruction(name):
    client = create_client()
    client.delete_instruction(name)


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def cancel_operation(name):
    client = create_client()
    client.transport._operations_client.cancel_operation(name)


@backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=RETRY_DEADLINE)
def import_data(dataset_name, data_type, gcs_uri):
    import_sample.import_data(dataset_name, data_type, gcs_uri)
