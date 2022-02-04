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
# Generated code. DO NOT EDIT!
#
# Snippet for ExportData
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-datalabeling


# [START datalabeling_generated_datalabeling_v1beta1_DataLabelingService_ExportData_sync]
from google.cloud import datalabeling_v1beta1


def sample_export_data():
    # Create a client
    client = datalabeling_v1beta1.DataLabelingServiceClient()

    # Initialize request argument(s)
    request = datalabeling_v1beta1.ExportDataRequest(
        name="name_value",
        annotated_dataset="annotated_dataset_value",
    )

    # Make the request
    operation = client.export_data(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    print(response)

# [END datalabeling_generated_datalabeling_v1beta1_DataLabelingService_ExportData_sync]