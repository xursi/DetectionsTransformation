from typing import List, Literal, Optional, Union

from pydantic import BaseModel

from sdks.novavision.src.base.model import Config, Configs, Input, Inputs, Output, Outputs, Package, Request, Response, Detection, BoundingBox




class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "Detections"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "Detections"


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


class DetectionsFilteringExecutor(Config):
    name: Literal["DetectionsFiltering"] = "DetectionsFiltering"
    value: Union[FilteringRequest, FilteringResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Detections Filtering"
        json_schema_extra = {"target": {"value": 0}}


class ConfigAdjustmentTargetLabels(Config):
    name: Literal["targetLabels"] = "targetLabels"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["car, person"] = "car, person"

    class Config:
        title = "Target Labels"
        json_schema_extra = {"shortDescription": "Target labels to adjust. Leave empty to adjust all."}


class ConfigShiftX(Config):
    name: Literal["shiftX"] = "shiftX"
    value: float = 0.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Shift X (Pixels)"
        json_schema_extra = {"shortDescription": "Horizontal shift. Positive moves right, negative moves left."}


class ConfigShiftY(Config):
    name: Literal["shiftY"] = "shiftY"
    value: float = 0.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Shift Y (Pixels)"
        json_schema_extra = {"shortDescription": "Vertical shift. Positive moves down, negative moves up."}


class ConfigAdjustmentShift(Config):
    shiftX: ConfigShiftX
    shiftY: ConfigShiftY
    name: Literal["Shift"] = "Shift"
    value: Literal["Shift"] = "Shift"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Shift"


class ConfigScaleWidth(Config):
    name: Literal["scaleWidth"] = "scaleWidth"
    value: float = 1.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Scale Width (Multiplier)"
        json_schema_extra = {"shortDescription": "Width multiplier. E.g., 1.2 to enlarge by 20%."}


class ConfigScaleHeight(Config):
    name: Literal["scaleHeight"] = "scaleHeight"
    value: float = 1.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Scale Height (Multiplier)"
        json_schema_extra = {"shortDescription": "Height multiplier. E.g., 0.8 to shrink by 20%."}


class ConfigAdjustmentResize(Config):
    scaleWidth: ConfigScaleWidth
    scaleHeight: ConfigScaleHeight
    name: Literal["Resize"] = "Resize"
    value: Literal["Resize"] = "Resize"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Resize (Scale)"


class ConfigAdjustmentType(Config):
    name: Literal["adjustmentType"] = "adjustmentType"
    value: Union[ConfigAdjustmentShift, ConfigAdjustmentResize]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Adjustment Type"
        json_schema_extra = {"shortDescription": "Select whether to shift or resize the bounding boxes."}


class AdjustmentInputs(Inputs):
    inputDetections: InputDetections


class AdjustmentConfigs(Configs):
    targetLabels: ConfigAdjustmentTargetLabels
    adjustmentType: ConfigAdjustmentType


class AdjustmentOutputs(Outputs):
    outputDetections: OutputDetections


class AdjustmentRequest(Request):
    inputs: AdjustmentInputs
    configs: AdjustmentConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class AdjustmentResponse(Response):
    outputs: AdjustmentOutputs


class DetectionAdjustmentExecutor(Config):
    name: Literal["DetectionAdjustment"] = "DetectionAdjustment"
    value: Union[AdjustmentRequest, AdjustmentResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Detection Adjustment"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[DetectionsFilteringExecutor, DetectionAdjustmentExecutor]
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
