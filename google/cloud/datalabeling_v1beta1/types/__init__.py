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
from .annotation import (
    Annotation,
    AnnotationMetadata,
    AnnotationValue,
    BoundingPoly,
    ImageBoundingPolyAnnotation,
    ImageClassificationAnnotation,
    ImagePolylineAnnotation,
    ImageSegmentationAnnotation,
    NormalizedBoundingPoly,
    NormalizedPolyline,
    NormalizedVertex,
    ObjectTrackingFrame,
    OperatorMetadata,
    Polyline,
    SequentialSegment,
    TextClassificationAnnotation,
    TextEntityExtractionAnnotation,
    TimeSegment,
    Vertex,
    VideoClassificationAnnotation,
    VideoEventAnnotation,
    VideoObjectTrackingAnnotation,
    AnnotationSentiment,
    AnnotationSource,
    AnnotationType,
)
from .annotation_spec_set import (
    AnnotationSpec,
    AnnotationSpecSet,
)
from .data_labeling_service import (
    CreateAnnotationSpecSetRequest,
    CreateDatasetRequest,
    CreateEvaluationJobRequest,
    CreateInstructionRequest,
    DeleteAnnotatedDatasetRequest,
    DeleteAnnotationSpecSetRequest,
    DeleteDatasetRequest,
    DeleteEvaluationJobRequest,
    DeleteInstructionRequest,
    ExportDataRequest,
    GetAnnotatedDatasetRequest,
    GetAnnotationSpecSetRequest,
    GetDataItemRequest,
    GetDatasetRequest,
    GetEvaluationJobRequest,
    GetEvaluationRequest,
    GetExampleRequest,
    GetInstructionRequest,
    ImportDataRequest,
    LabelImageRequest,
    LabelTextRequest,
    LabelVideoRequest,
    ListAnnotatedDatasetsRequest,
    ListAnnotatedDatasetsResponse,
    ListAnnotationSpecSetsRequest,
    ListAnnotationSpecSetsResponse,
    ListDataItemsRequest,
    ListDataItemsResponse,
    ListDatasetsRequest,
    ListDatasetsResponse,
    ListEvaluationJobsRequest,
    ListEvaluationJobsResponse,
    ListExamplesRequest,
    ListExamplesResponse,
    ListInstructionsRequest,
    ListInstructionsResponse,
    PauseEvaluationJobRequest,
    ResumeEvaluationJobRequest,
    SearchEvaluationsRequest,
    SearchEvaluationsResponse,
    SearchExampleComparisonsRequest,
    SearchExampleComparisonsResponse,
    UpdateEvaluationJobRequest,
)
from .data_payloads import (
    ImagePayload,
    TextPayload,
    VideoPayload,
    VideoThumbnail,
)
from .dataset import (
    AnnotatedDataset,
    AnnotatedDatasetMetadata,
    BigQuerySource,
    ClassificationMetadata,
    DataItem,
    Dataset,
    Example,
    GcsDestination,
    GcsFolderDestination,
    GcsSource,
    InputConfig,
    LabelStats,
    OutputConfig,
    TextMetadata,
    DataType,
)
from .evaluation import (
    BoundingBoxEvaluationOptions,
    ClassificationMetrics,
    ConfusionMatrix,
    Evaluation,
    EvaluationConfig,
    EvaluationMetrics,
    ObjectDetectionMetrics,
    PrCurve,
)
from .evaluation_job import (
    Attempt,
    EvaluationJob,
    EvaluationJobAlertConfig,
    EvaluationJobConfig,
)
from .human_annotation_config import (
    BoundingPolyConfig,
    EventConfig,
    HumanAnnotationConfig,
    ImageClassificationConfig,
    ObjectDetectionConfig,
    ObjectTrackingConfig,
    PolylineConfig,
    SegmentationConfig,
    SentimentConfig,
    TextClassificationConfig,
    TextEntityExtractionConfig,
    VideoClassificationConfig,
    StringAggregationType,
)
from .instruction import (
    CsvInstruction,
    Instruction,
    PdfInstruction,
)
from .operations import (
    CreateInstructionMetadata,
    ExportDataOperationMetadata,
    ExportDataOperationResponse,
    ImportDataOperationMetadata,
    ImportDataOperationResponse,
    LabelImageBoundingBoxOperationMetadata,
    LabelImageBoundingPolyOperationMetadata,
    LabelImageClassificationOperationMetadata,
    LabelImageOrientedBoundingBoxOperationMetadata,
    LabelImagePolylineOperationMetadata,
    LabelImageSegmentationOperationMetadata,
    LabelOperationMetadata,
    LabelTextClassificationOperationMetadata,
    LabelTextEntityExtractionOperationMetadata,
    LabelVideoClassificationOperationMetadata,
    LabelVideoEventOperationMetadata,
    LabelVideoObjectDetectionOperationMetadata,
    LabelVideoObjectTrackingOperationMetadata,
)

__all__ = (
    "Annotation",
    "AnnotationMetadata",
    "AnnotationValue",
    "BoundingPoly",
    "ImageBoundingPolyAnnotation",
    "ImageClassificationAnnotation",
    "ImagePolylineAnnotation",
    "ImageSegmentationAnnotation",
    "NormalizedBoundingPoly",
    "NormalizedPolyline",
    "NormalizedVertex",
    "ObjectTrackingFrame",
    "OperatorMetadata",
    "Polyline",
    "SequentialSegment",
    "TextClassificationAnnotation",
    "TextEntityExtractionAnnotation",
    "TimeSegment",
    "Vertex",
    "VideoClassificationAnnotation",
    "VideoEventAnnotation",
    "VideoObjectTrackingAnnotation",
    "AnnotationSentiment",
    "AnnotationSource",
    "AnnotationType",
    "AnnotationSpec",
    "AnnotationSpecSet",
    "CreateAnnotationSpecSetRequest",
    "CreateDatasetRequest",
    "CreateEvaluationJobRequest",
    "CreateInstructionRequest",
    "DeleteAnnotatedDatasetRequest",
    "DeleteAnnotationSpecSetRequest",
    "DeleteDatasetRequest",
    "DeleteEvaluationJobRequest",
    "DeleteInstructionRequest",
    "ExportDataRequest",
    "GetAnnotatedDatasetRequest",
    "GetAnnotationSpecSetRequest",
    "GetDataItemRequest",
    "GetDatasetRequest",
    "GetEvaluationJobRequest",
    "GetEvaluationRequest",
    "GetExampleRequest",
    "GetInstructionRequest",
    "ImportDataRequest",
    "LabelImageRequest",
    "LabelTextRequest",
    "LabelVideoRequest",
    "ListAnnotatedDatasetsRequest",
    "ListAnnotatedDatasetsResponse",
    "ListAnnotationSpecSetsRequest",
    "ListAnnotationSpecSetsResponse",
    "ListDataItemsRequest",
    "ListDataItemsResponse",
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "ListEvaluationJobsRequest",
    "ListEvaluationJobsResponse",
    "ListExamplesRequest",
    "ListExamplesResponse",
    "ListInstructionsRequest",
    "ListInstructionsResponse",
    "PauseEvaluationJobRequest",
    "ResumeEvaluationJobRequest",
    "SearchEvaluationsRequest",
    "SearchEvaluationsResponse",
    "SearchExampleComparisonsRequest",
    "SearchExampleComparisonsResponse",
    "UpdateEvaluationJobRequest",
    "ImagePayload",
    "TextPayload",
    "VideoPayload",
    "VideoThumbnail",
    "AnnotatedDataset",
    "AnnotatedDatasetMetadata",
    "BigQuerySource",
    "ClassificationMetadata",
    "DataItem",
    "Dataset",
    "Example",
    "GcsDestination",
    "GcsFolderDestination",
    "GcsSource",
    "InputConfig",
    "LabelStats",
    "OutputConfig",
    "TextMetadata",
    "DataType",
    "BoundingBoxEvaluationOptions",
    "ClassificationMetrics",
    "ConfusionMatrix",
    "Evaluation",
    "EvaluationConfig",
    "EvaluationMetrics",
    "ObjectDetectionMetrics",
    "PrCurve",
    "Attempt",
    "EvaluationJob",
    "EvaluationJobAlertConfig",
    "EvaluationJobConfig",
    "BoundingPolyConfig",
    "EventConfig",
    "HumanAnnotationConfig",
    "ImageClassificationConfig",
    "ObjectDetectionConfig",
    "ObjectTrackingConfig",
    "PolylineConfig",
    "SegmentationConfig",
    "SentimentConfig",
    "TextClassificationConfig",
    "TextEntityExtractionConfig",
    "VideoClassificationConfig",
    "StringAggregationType",
    "CsvInstruction",
    "Instruction",
    "PdfInstruction",
    "CreateInstructionMetadata",
    "ExportDataOperationMetadata",
    "ExportDataOperationResponse",
    "ImportDataOperationMetadata",
    "ImportDataOperationResponse",
    "LabelImageBoundingBoxOperationMetadata",
    "LabelImageBoundingPolyOperationMetadata",
    "LabelImageClassificationOperationMetadata",
    "LabelImageOrientedBoundingBoxOperationMetadata",
    "LabelImagePolylineOperationMetadata",
    "LabelImageSegmentationOperationMetadata",
    "LabelOperationMetadata",
    "LabelTextClassificationOperationMetadata",
    "LabelTextEntityExtractionOperationMetadata",
    "LabelVideoClassificationOperationMetadata",
    "LabelVideoEventOperationMetadata",
    "LabelVideoObjectDetectionOperationMetadata",
    "LabelVideoObjectTrackingOperationMetadata",
)
