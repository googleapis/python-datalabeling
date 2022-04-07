# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
# Snippet for LabelVideo
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-datalabeling


# [START datalabeling_v1beta1_generated_DataLabelingService_LabelVideo_async]
from google.cloud import datalabeling_v1beta1


async def sample_label_video():
    # Create a client
    client = datalabeling_v1beta1.DataLabelingServiceAsyncClient()

    # Initialize request argument(s)
    video_classification_config = datalabeling_v1beta1.VideoClassificationConfig()
    video_classification_config.annotation_spec_set_configs.annotation_spec_set = "annotation_spec_set_value"

    basic_config = datalabeling_v1beta1.HumanAnnotationConfig()
    basic_config.instruction = "instruction_value"
    basic_config.annotated_dataset_display_name = "annotated_dataset_display_name_value"

    request = datalabeling_v1beta1.LabelVideoRequest(
        video_classification_config=video_classification_config,
        parent="parent_value",
        basic_config=basic_config,
        feature="EVENT",
    )

    # Make the request
    operation = client.label_video(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()

    # Handle the response
    print(response)

# [END datalabeling_v1beta1_generated_DataLabelingService_LabelVideo_async]
