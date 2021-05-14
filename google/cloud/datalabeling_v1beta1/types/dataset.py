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
import proto  # type: ignore

from google.cloud.datalabeling_v1beta1.types import annotation
from google.cloud.datalabeling_v1beta1.types import data_payloads
from google.cloud.datalabeling_v1beta1.types import (
    human_annotation_config as gcd_human_annotation_config,
)
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.datalabeling.v1beta1",
    manifest={
        "DataType",
        "Dataset",
        "InputConfig",
        "TextMetadata",
        "ClassificationMetadata",
        "GcsSource",
        "BigQuerySource",
        "OutputConfig",
        "GcsDestination",
        "GcsFolderDestination",
        "DataItem",
        "AnnotatedDataset",
        "LabelStats",
        "AnnotatedDatasetMetadata",
        "Example",
    },
)


class DataType(proto.Enum):
    r""""""
    DATA_TYPE_UNSPECIFIED = 0
    IMAGE = 1
    VIDEO = 2
    TEXT = 4
    GENERAL_DATA = 6


class Dataset(proto.Message):
    r"""Dataset is the resource to hold your data. You can request
    multiple labeling tasks for a dataset while each one will
    generate an AnnotatedDataset.

    Attributes:
        name (str):
            Output only. Dataset resource name, format is:
            projects/{project_id}/datasets/{dataset_id}
        display_name (str):
            Required. The display name of the dataset.
            Maximum of 64 characters.
        description (str):
            Optional. User-provided description of the
            annotation specification set. The description
            can be up to 10000 characters long.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the dataset is created.
        input_configs (Sequence[google.cloud.datalabeling_v1beta1.types.InputConfig]):
            Output only. This is populated with the
            original input configs where ImportData is
            called. It is available only after the clients
            import data to this dataset.
        blocking_resources (Sequence[str]):
            Output only. The names of any related
            resources that are blocking changes to the
            dataset.
        data_item_count (int):
            Output only. The number of data items in the
            dataset.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    input_configs = proto.RepeatedField(proto.MESSAGE, number=5, message="InputConfig",)
    blocking_resources = proto.RepeatedField(proto.STRING, number=6,)
    data_item_count = proto.Field(proto.INT64, number=7,)


class InputConfig(proto.Message):
    r"""The configuration of input data, including data type,
    location, etc.

    Attributes:
        text_metadata (google.cloud.datalabeling_v1beta1.types.TextMetadata):
            Required for text import, as language code
            must be specified.
        gcs_source (google.cloud.datalabeling_v1beta1.types.GcsSource):
            Source located in Cloud Storage.
        bigquery_source (google.cloud.datalabeling_v1beta1.types.BigQuerySource):
            Source located in BigQuery. You must specify this field if
            you are using this InputConfig in an
            [EvaluationJob][google.cloud.datalabeling.v1beta1.EvaluationJob].
        data_type (google.cloud.datalabeling_v1beta1.types.DataType):
            Required. Data type must be specifed when
            user tries to import data.
        annotation_type (google.cloud.datalabeling_v1beta1.types.AnnotationType):
            Optional. The type of annotation to be performed on this
            data. You must specify this field if you are using this
            InputConfig in an
            [EvaluationJob][google.cloud.datalabeling.v1beta1.EvaluationJob].
        classification_metadata (google.cloud.datalabeling_v1beta1.types.ClassificationMetadata):
            Optional. Metadata about annotations for the input. You must
            specify this field if you are using this InputConfig in an
            [EvaluationJob][google.cloud.datalabeling.v1beta1.EvaluationJob]
            for a model version that performs classification.
    """

    text_metadata = proto.Field(
        proto.MESSAGE, number=6, oneof="data_type_metadata", message="TextMetadata",
    )
    gcs_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message="GcsSource",
    )
    bigquery_source = proto.Field(
        proto.MESSAGE, number=5, oneof="source", message="BigQuerySource",
    )
    data_type = proto.Field(proto.ENUM, number=1, enum="DataType",)
    annotation_type = proto.Field(proto.ENUM, number=3, enum=annotation.AnnotationType,)
    classification_metadata = proto.Field(
        proto.MESSAGE, number=4, message="ClassificationMetadata",
    )


class TextMetadata(proto.Message):
    r"""Metadata for the text.
    Attributes:
        language_code (str):
            The language of this text, as a
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__.
            Default value is en-US.
    """

    language_code = proto.Field(proto.STRING, number=1,)


class ClassificationMetadata(proto.Message):
    r"""Metadata for classification annotations.
    Attributes:
        is_multi_label (bool):
            Whether the classification task is multi-
            abel or not.
    """

    is_multi_label = proto.Field(proto.BOOL, number=1,)


class GcsSource(proto.Message):
    r"""Source of the Cloud Storage file to be imported.
    Attributes:
        input_uri (str):
            Required. The input URI of source file. This must be a Cloud
            Storage path (``gs://...``).
        mime_type (str):
            Required. The format of the source file. Only
            "text/csv" is supported.
    """

    input_uri = proto.Field(proto.STRING, number=1,)
    mime_type = proto.Field(proto.STRING, number=2,)


class BigQuerySource(proto.Message):
    r"""The BigQuery location for input data. If used in an
    [EvaluationJob][google.cloud.datalabeling.v1beta1.EvaluationJob],
    this is where the service saves the prediction input and output
    sampled from the model version.

    Attributes:
        input_uri (str):
            Required. BigQuery URI to a table, up to 2,000 characters
            long. If you specify the URI of a table that does not exist,
            Data Labeling Service creates a table at the URI with the
            correct schema when you create your
            [EvaluationJob][google.cloud.datalabeling.v1beta1.EvaluationJob].
            If you specify the URI of a table that already exists, it
            must have the `correct
            schema </ml-engine/docs/continuous-evaluation/create-job#table-schema>`__.

            Provide the table URI in the following format:

            "bq://{your_project_id}/{your_dataset_name}/{your_table_name}"

            `Learn
            more </ml-engine/docs/continuous-evaluation/create-job#table-schema>`__.
    """

    input_uri = proto.Field(proto.STRING, number=1,)


class OutputConfig(proto.Message):
    r"""The configuration of output data.
    Attributes:
        gcs_destination (google.cloud.datalabeling_v1beta1.types.GcsDestination):
            Output to a file in Cloud Storage. Should be
            used for labeling output other than image
            segmentation.
        gcs_folder_destination (google.cloud.datalabeling_v1beta1.types.GcsFolderDestination):
            Output to a folder in Cloud Storage. Should
            be used for image segmentation labeling output.
    """

    gcs_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message="GcsDestination",
    )
    gcs_folder_destination = proto.Field(
        proto.MESSAGE, number=2, oneof="destination", message="GcsFolderDestination",
    )


class GcsDestination(proto.Message):
    r"""Export destination of the data.Only gcs path is allowed in
    output_uri.

    Attributes:
        output_uri (str):
            Required. The output uri of destination file.
        mime_type (str):
            Required. The format of the gcs destination.
            Only "text/csv" and "application/json"
            are supported.
    """

    output_uri = proto.Field(proto.STRING, number=1,)
    mime_type = proto.Field(proto.STRING, number=2,)


class GcsFolderDestination(proto.Message):
    r"""Export folder destination of the data.
    Attributes:
        output_folder_uri (str):
            Required. Cloud Storage directory to export
            data to.
    """

    output_folder_uri = proto.Field(proto.STRING, number=1,)


class DataItem(proto.Message):
    r"""DataItem is a piece of data, without annotation. For example,
    an image.

    Attributes:
        image_payload (google.cloud.datalabeling_v1beta1.types.ImagePayload):
            The image payload, a container of the image
            bytes/uri.
        text_payload (google.cloud.datalabeling_v1beta1.types.TextPayload):
            The text payload, a container of text
            content.
        video_payload (google.cloud.datalabeling_v1beta1.types.VideoPayload):
            The video payload, a container of the video
            uri.
        name (str):
            Output only. Name of the data item, in format of:
            projects/{project_id}/datasets/{dataset_id}/dataItems/{data_item_id}
    """

    image_payload = proto.Field(
        proto.MESSAGE, number=2, oneof="payload", message=data_payloads.ImagePayload,
    )
    text_payload = proto.Field(
        proto.MESSAGE, number=3, oneof="payload", message=data_payloads.TextPayload,
    )
    video_payload = proto.Field(
        proto.MESSAGE, number=4, oneof="payload", message=data_payloads.VideoPayload,
    )
    name = proto.Field(proto.STRING, number=1,)


class AnnotatedDataset(proto.Message):
    r"""AnnotatedDataset is a set holding annotations for data in a
    Dataset. Each labeling task will generate an AnnotatedDataset
    under the Dataset that the task is requested for.

    Attributes:
        name (str):
            Output only. AnnotatedDataset resource name in format of:
            projects/{project_id}/datasets/{dataset_id}/annotatedDatasets/
            {annotated_dataset_id}
        display_name (str):
            Output only. The display name of the
            AnnotatedDataset. It is specified in
            HumanAnnotationConfig when user starts a
            labeling task. Maximum of 64 characters.
        description (str):
            Output only. The description of the
            AnnotatedDataset. It is specified in
            HumanAnnotationConfig when user starts a
            labeling task. Maximum of 10000 characters.
        annotation_source (google.cloud.datalabeling_v1beta1.types.AnnotationSource):
            Output only. Source of the annotation.
        annotation_type (google.cloud.datalabeling_v1beta1.types.AnnotationType):
            Output only. Type of the annotation. It is
            specified when starting labeling task.
        example_count (int):
            Output only. Number of examples in the
            annotated dataset.
        completed_example_count (int):
            Output only. Number of examples that have
            annotation in the annotated dataset.
        label_stats (google.cloud.datalabeling_v1beta1.types.LabelStats):
            Output only. Per label statistics.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the AnnotatedDataset was
            created.
        metadata (google.cloud.datalabeling_v1beta1.types.AnnotatedDatasetMetadata):
            Output only. Additional information about
            AnnotatedDataset.
        blocking_resources (Sequence[str]):
            Output only. The names of any related
            resources that are blocking changes to the
            annotated dataset.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=9,)
    annotation_source = proto.Field(
        proto.ENUM, number=3, enum=annotation.AnnotationSource,
    )
    annotation_type = proto.Field(proto.ENUM, number=8, enum=annotation.AnnotationType,)
    example_count = proto.Field(proto.INT64, number=4,)
    completed_example_count = proto.Field(proto.INT64, number=5,)
    label_stats = proto.Field(proto.MESSAGE, number=6, message="LabelStats",)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    metadata = proto.Field(
        proto.MESSAGE, number=10, message="AnnotatedDatasetMetadata",
    )
    blocking_resources = proto.RepeatedField(proto.STRING, number=11,)


class LabelStats(proto.Message):
    r"""Statistics about annotation specs.
    Attributes:
        example_count (Sequence[google.cloud.datalabeling_v1beta1.types.LabelStats.ExampleCountEntry]):
            Map of each annotation spec's example count.
            Key is the annotation spec name and value is the
            number of examples for that annotation spec. If
            the annotated dataset does not have annotation
            spec, the map will return a pair where the key
            is empty string and value is the total number of
            annotations.
    """

    example_count = proto.MapField(proto.STRING, proto.INT64, number=1,)


class AnnotatedDatasetMetadata(proto.Message):
    r"""Metadata on AnnotatedDataset.
    Attributes:
        image_classification_config (google.cloud.datalabeling_v1beta1.types.ImageClassificationConfig):
            Configuration for image classification task.
        bounding_poly_config (google.cloud.datalabeling_v1beta1.types.BoundingPolyConfig):
            Configuration for image bounding box and
            bounding poly task.
        polyline_config (google.cloud.datalabeling_v1beta1.types.PolylineConfig):
            Configuration for image polyline task.
        segmentation_config (google.cloud.datalabeling_v1beta1.types.SegmentationConfig):
            Configuration for image segmentation task.
        video_classification_config (google.cloud.datalabeling_v1beta1.types.VideoClassificationConfig):
            Configuration for video classification task.
        object_detection_config (google.cloud.datalabeling_v1beta1.types.ObjectDetectionConfig):
            Configuration for video object detection
            task.
        object_tracking_config (google.cloud.datalabeling_v1beta1.types.ObjectTrackingConfig):
            Configuration for video object tracking task.
        event_config (google.cloud.datalabeling_v1beta1.types.EventConfig):
            Configuration for video event labeling task.
        text_classification_config (google.cloud.datalabeling_v1beta1.types.TextClassificationConfig):
            Configuration for text classification task.
        text_entity_extraction_config (google.cloud.datalabeling_v1beta1.types.TextEntityExtractionConfig):
            Configuration for text entity extraction
            task.
        human_annotation_config (google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig):
            HumanAnnotationConfig used when requesting
            the human labeling task for this
            AnnotatedDataset.
    """

    image_classification_config = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.ImageClassificationConfig,
    )
    bounding_poly_config = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.BoundingPolyConfig,
    )
    polyline_config = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.PolylineConfig,
    )
    segmentation_config = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.SegmentationConfig,
    )
    video_classification_config = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.VideoClassificationConfig,
    )
    object_detection_config = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.ObjectDetectionConfig,
    )
    object_tracking_config = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.ObjectTrackingConfig,
    )
    event_config = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.EventConfig,
    )
    text_classification_config = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.TextClassificationConfig,
    )
    text_entity_extraction_config = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="annotation_request_config",
        message=gcd_human_annotation_config.TextEntityExtractionConfig,
    )
    human_annotation_config = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_human_annotation_config.HumanAnnotationConfig,
    )


class Example(proto.Message):
    r"""An Example is a piece of data and its annotation. For
    example, an image with label "house".

    Attributes:
        image_payload (google.cloud.datalabeling_v1beta1.types.ImagePayload):
            The image payload, a container of the image
            bytes/uri.
        text_payload (google.cloud.datalabeling_v1beta1.types.TextPayload):
            The text payload, a container of the text
            content.
        video_payload (google.cloud.datalabeling_v1beta1.types.VideoPayload):
            The video payload, a container of the video
            uri.
        name (str):
            Output only. Name of the example, in format of:
            projects/{project_id}/datasets/{dataset_id}/annotatedDatasets/
            {annotated_dataset_id}/examples/{example_id}
        annotations (Sequence[google.cloud.datalabeling_v1beta1.types.Annotation]):
            Output only. Annotations for the piece of
            data in Example. One piece of data can have
            multiple annotations.
    """

    image_payload = proto.Field(
        proto.MESSAGE, number=2, oneof="payload", message=data_payloads.ImagePayload,
    )
    text_payload = proto.Field(
        proto.MESSAGE, number=6, oneof="payload", message=data_payloads.TextPayload,
    )
    video_payload = proto.Field(
        proto.MESSAGE, number=7, oneof="payload", message=data_payloads.VideoPayload,
    )
    name = proto.Field(proto.STRING, number=1,)
    annotations = proto.RepeatedField(
        proto.MESSAGE, number=5, message=annotation.Annotation,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
