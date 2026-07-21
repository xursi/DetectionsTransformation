from sdks.novavision.src.helper.package import PackageHelper

from src.models.PackageModel import (
    ConfigExecutor,
    OutputDetections,
    PackageConfigs,
    PackageModel,
    TransformationExecutor,
    TransformationOutputs,
    TransformationResponse,
)


def build_response(context):
    outputs = TransformationOutputs(outputDetections=OutputDetections(value=context.detections))
    response = TransformationResponse(outputs=outputs)
    executor = ConfigExecutor(value=TransformationExecutor(value=response))
    package_configs = PackageConfigs(executor=executor)
    return PackageHelper(packageModel=PackageModel, packageConfigs=package_configs).build_model(context)
