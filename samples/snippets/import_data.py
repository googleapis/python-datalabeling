#!/usr/bin/env python

# Copyright 2019 Google LLC
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

import argparse
import os

from google.api_core.client_options import ClientOptions


# [START datalabeling_import_data_beta]
def import_data(project_id, dataset_id, data_type, input_gcs_uri):
    """Imports data to the given Google Cloud project and dataset."""
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_import_data_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_import_data_beta]

    name = client.dataset_path(project_id, dataset_id)

    gcs_source = datalabeling.types.GcsSource(
        input_uri=input_gcs_uri, mime_type="text/csv"
    )

    input_config = datalabeling.types.InputConfig(
        data_type=data_type, gcs_source=gcs_source
    )

    response = client.import_data(name, input_config)

    result = response.result()

    print("Dataset resource name: {}\n".format(result.dataset))

    return result


# [END datalabeling_import_data_beta]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--project-id",
        help="The project id.",
        required=True,
    )
    parser.add_argument(
        "--dataset-id",
        help="Dataset id. Required.",
        required=True,
    )

    parser.add_argument(
        "--data-type",
        help="Data type. Only support IMAGE, VIDEO, TEXT and AUDIO. Required.",
        required=True,
    )

    parser.add_argument(
        "--input-gcs-uri",
        help="The GCS URI of the input dataset. Required.",
        required=True,
    )

    args = parser.parse_args()

    import_data(args.project_id, args.dataset_id, args.data_type, args.input_gcs_uri)
