from sdks.novavision.src.helper.package import PackageHelper

from components.DetectionTransformation.src.models.PackageModel import ConfigExecutor, FilteringExecutor, FilteringOutputs, FilteringResponse, OutputDetections, PackageConfigs, PackageModel



def build_response(context):
    outputs = FilteringOutputs(outputDetections=OutputDetections(value=context.detections))
    response = FilteringResponse(outputs=outputs)
    executor = ConfigExecutor(value=FilteringExecutor(value=response))
    package_configs = PackageConfigs(executor=executor)
    return PackageHelper(packageModel=PackageModel, packageConfigs=package_configs).build_model(context)
