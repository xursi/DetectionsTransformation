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
    """
    Specifies the list of class labels to be allowed through the filter.
    Input labels should be separated by commas (e.g. 'person, car'). Leave empty to allow all detections.
    """
    name: Literal["allowedLabels"] = "allowedLabels"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["person, car, tie"] = "person, car, tie"

    class Config:
        title = "Allowed Labels"
        json_schema_extra = {
            "shortDescription": "Filter Labels List"
        }


class ConfigFilterByLabel(Config):
    allowedLabels: ConfigAllowedLabels
    name: Literal["FilterByLabel"] = "FilterByLabel"
    value: Literal["FilterByLabel"] = "FilterByLabel"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "By Label"


class ConfigFilterType(Config):
    """
    Specifies the criteria to filter detections.
    Currently supports filtering by class labels.
    """
    name: Literal["filterType"] = "filterType"
    value: ConfigFilterByLabel
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Filter Type"
        json_schema_extra = {
            "shortDescription": "Filter Criteria Type"
        }


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
    """
    Filters incoming object detections based on specific conditions such as allowed class labels.
    """
    name: Literal["DetectionsFiltering"] = "DetectionsFiltering"
    value: Union[FilteringRequest, FilteringResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Detections Filtering"
        json_schema_extra = {
            "target": {"value": 0},
            "shortDescription": "Detections Filtering"
        }


class ConfigAdjustmentTargetLabels(Config):
    """
    Specifies which class labels should undergo shifting or resizing.
    Provide a comma-separated list of labels. If left empty, the transformation applies to all detections.
    """
    name: Literal["targetLabels"] = "targetLabels"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["car, person"] = "car, person"

    class Config:
        title = "Target Labels"
        json_schema_extra = {
            "shortDescription": "Target Detections Labels"
        }


class ConfigShiftX(Config):
    """
    The horizontal pixel distance to shift the bounding box.
    Positive values shift the box to the right, negative values shift it to the left.
    """
    name: Literal["shiftX"] = "shiftX"
    value: float = 0.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Shift X (Pixels)"
        json_schema_extra = {
            "shortDescription": "Horizontal Shift (px)"
        }


class ConfigShiftY(Config):
    """
    The vertical pixel distance to shift the bounding box.
    Positive values shift the box downwards, negative values shift it upwards.
    """
    name: Literal["shiftY"] = "shiftY"
    value: float = 0.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Shift Y (Pixels)"
        json_schema_extra = {
            "shortDescription": "Vertical Shift (px)"
        }


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
    """
    The multiplier coefficient to scale the width of the bounding box.
    Values greater than 1.0 enlarge the box width, values less than 1.0 shrink it.
    """
    name: Literal["scaleWidth"] = "scaleWidth"
    value: float = 1.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Scale Width (Multiplier)"
        json_schema_extra = {
            "shortDescription": "Width Multiplier"
        }


class ConfigScaleHeight(Config):
    """
    The multiplier coefficient to scale the height of the bounding box.
    Values greater than 1.0 enlarge the box height, values less than 1.0 shrink it.
    """
    name: Literal["scaleHeight"] = "scaleHeight"
    value: float = 1.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Scale Height (Multiplier)"
        json_schema_extra = {
            "shortDescription": "Height Multiplier"
        }


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
    """
    Selects the geometric adjustment operation to perform on the bounding boxes.
    Choose 'Shift' to translate the position or 'Resize' to scale the dimensions.
    """
    name: Literal["adjustmentType"] = "adjustmentType"
    value: Union[ConfigAdjustmentShift, ConfigAdjustmentResize]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Adjustment Type"
        json_schema_extra = {
            "shortDescription": "Box Transformation Type"
        }


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
    """
    Adjusts the coordinates of bounding boxes by shifting their positions or scaling their dimensions.
    """
    name: Literal["DetectionAdjustment"] = "DetectionAdjustment"
    value: Union[AdjustmentRequest, AdjustmentResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Detection Adjustment"
        json_schema_extra = {
            "target": {"value": 0},
            "shortDescription": "Detection Coordinate Adjustment"
        }


class ConfigExecutor(Config):
    """
    The primary task execution mode of the component.
    Select 'Detections Filtering' to drop classes, or 'Detection Adjustment' to transform bounding boxes.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[DetectionsFilteringExecutor, DetectionAdjustmentExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "shortDescription": "Transformation Action"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DetectionTransformation"] = "DetectionTransformation"
