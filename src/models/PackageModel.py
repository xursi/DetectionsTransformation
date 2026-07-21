from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from sdks.novavision.src.base.model import Config, Configs, Input, Inputs, Output, Outputs, Package, Request, Response


class BoundingBox(BaseModel):
    left: float
    top: float
    width: float
    height: float


class Detection(BaseModel):
    boundingBox: BoundingBox
    confidence: float
    classLabel: str
    classId: int
    keyPoints: Optional[object] = None
    imgUID: str


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "YOLO Detections"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "Transformed Detections"


class ConfigMinConfidence(Config):
    name: Literal["minConfidence"] = "minConfidence"
    value: float = Field(default=0.0, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Minimum Confidence"
        json_schema_extra = {"shortDescription": "Keep detections with this score or higher. 0 disables the limit."}


class ConfigMaxConfidence(Config):
    name: Literal["maxConfidence"] = "maxConfidence"
    value: float = Field(default=1.0, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Maximum Confidence"
        json_schema_extra = {"shortDescription": "Keep detections with this score or lower. 1 disables the limit."}


class ConfigAllowedLabels(Config):
    name: Literal["allowedLabels"] = "allowedLabels"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["person, car, tie"] = "person, car, tie"

    class Config:
        title = "Allowed Labels"
        json_schema_extra = {"shortDescription": "Comma-separated labels to keep. Leave empty to keep all labels."}


class ConfigRenameSourceLabel(Config):
    name: Literal["renameSourceLabel"] = "renameSourceLabel"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Rename Source Label"


class ConfigRenameTargetLabel(Config):
    name: Literal["renameTargetLabel"] = "renameTargetLabel"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Rename Target Label"


class TransformationInputs(Inputs):
    inputDetections: InputDetections


class TransformationConfigs(Configs):
    minConfidence: ConfigMinConfidence
    maxConfidence: ConfigMaxConfidence
    allowedLabels: ConfigAllowedLabels
    renameSourceLabel: ConfigRenameSourceLabel
    renameTargetLabel: ConfigRenameTargetLabel


class TransformationOutputs(Outputs):
    outputDetections: OutputDetections


class TransformationRequest(Request):
    inputs: TransformationInputs
    configs: TransformationConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class TransformationResponse(Response):
    outputs: TransformationOutputs


class TransformationExecutor(Config):
    name: Literal["DetectionTransformation"] = "DetectionTransformation"
    value: Union[TransformationRequest, TransformationResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Detection Transformation"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: TransformationExecutor
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DetectionTransformation"] = "DetectionTransformation"
