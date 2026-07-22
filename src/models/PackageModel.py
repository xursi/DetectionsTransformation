from typing import List, Literal, Optional, Union

from pydantic import BaseModel

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


class ConfigAllowedLabels(Config):
    name: Literal["allowedLabels"] = "allowedLabels"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["person, car, tie"] = "person, car, tie"

    class Config:
        title = "Allowed Labels"
        json_schema_extra = {"shortDescription": "Comma-separated labels to keep. Leave empty to keep all labels."}


class ConfigFilterByLabel(Config):
    allowedLabels: ConfigAllowedLabels
    name: Literal["FilterByLabel"] = "FilterByLabel"
    value: Literal["FilterByLabel"] = "FilterByLabel"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "By Label"


class ConfigFilterType(Config):
    name: Literal["filterType"] = "filterType"
    value: ConfigFilterByLabel
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Filter Type"
        json_schema_extra = {"shortDescription": "Choose the detection field used for filtering."}


class FilteringInputs(Inputs):
    inputDetections: InputDetections


class FilteringConfigs(Configs):
    filterType: ConfigFilterType


class FilteringOutputs(Outputs):
    outputDetections: OutputDetections


class FilteringRequest(Request):
    inputs: FilteringInputs
    configs: FilteringConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class FilteringResponse(Response):
    outputs: FilteringOutputs


class FilteringExecutor(Config):
    name: Literal["Filtering"] = "Filtering"
    value: Union[FilteringRequest, FilteringResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Filtering"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: FilteringExecutor
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
