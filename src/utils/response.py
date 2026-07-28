from sdks.novavision.src.helper.package import PackageHelper

from components.DetectionTransformation.src.models.PackageModel import (
    ConfigExecutor,
    DetectionsFilteringExecutor,
    FilteringOutputs,
    FilteringResponse,
    OutputDetections,
    PackageConfigs,
    PackageModel,
    DetectionAdjustmentExecutor,
    AdjustmentOutputs,
    AdjustmentResponse,
    SortDetectionExecutor,
    SortOutputs,
    SortDetectionResponse
)


def build_filtering_response(context):
    outputs = FilteringOutputs(outputDetections=OutputDetections(value=context.detections))
    response = FilteringResponse(outputs=outputs)
    executor = ConfigExecutor(value=DetectionsFilteringExecutor(value=response))
    package_configs = PackageConfigs(executor=executor)
    return PackageHelper(packageModel=PackageModel, packageConfigs=package_configs).build_model(context)


def build_adjustment_response(context):
    outputs = AdjustmentOutputs(outputDetections=OutputDetections(value=context.detections))
    response = AdjustmentResponse(outputs=outputs)
    executor = ConfigExecutor(value=DetectionAdjustmentExecutor(value=response))
    package_configs = PackageConfigs(executor=executor)
    return PackageHelper(packageModel=PackageModel, packageConfigs=package_configs).build_model(context)


def build_sort_response(context):
    outputs = SortOutputs(outputDetections=OutputDetections(value=context.detections))
    response = SortDetectionResponse(outputs=outputs)
    executor = ConfigExecutor(value=SortDetectionExecutor(value=response))
    package_configs = PackageConfigs(executor=executor)
    return PackageHelper(packageModel=PackageModel, packageConfigs=package_configs).build_model(context)
