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


# --- Detections Filtering Classes ---

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


# --- Detection Adjustment Classes ---

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


# --- Sort Detection Classes ---

class ConfigSortByXMin(Config):
    name: Literal["x_min"] = "x_min"
    value: Literal["x_min"] = "x_min"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "X Min"


class ConfigSortByXMax(Config):
    name: Literal["x_max"] = "x_max"
    value: Literal["x_max"] = "x_max"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "X Max"


class ConfigSortByYMin(Config):
    name: Literal["y_min"] = "y_min"
    value: Literal["y_min"] = "y_min"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Y Min"


class ConfigSortByYMax(Config):
    name: Literal["y_max"] = "y_max"
    value: Literal["y_max"] = "y_max"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Y Max"


class ConfigSortBySize(Config):
    name: Literal["size"] = "size"
    value: Literal["size"] = "size"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Size (Area)"


class ConfigSortByCenterX(Config):
    name: Literal["center_x"] = "center_x"
    value: Literal["center_x"] = "center_x"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Center X"


class ConfigSortByCenterY(Config):
    name: Literal["center_y"] = "center_y"
    value: Literal["center_y"] = "center_y"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Center Y"


class ConfigSortByConfidence(Config):
    name: Literal["confidence"] = "confidence"
    value: Literal["confidence"] = "confidence"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Confidence"


class ConfigSortBy(Config):
    """
    Selects the attribute of the bounding box or metadata to sort the detections by.
    """
    name: Literal["sortBy"] = "sortBy"
    value: Union[
        ConfigSortByXMin, 
        ConfigSortByXMax, 
        ConfigSortByYMin, 
        ConfigSortByYMax, 
        ConfigSortBySize, 
        ConfigSortByCenterX, 
        ConfigSortByCenterY,
        ConfigSortByConfidence
    ]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Sort By"
        json_schema_extra = {
            "shortDescription": "Sort Attribute"
        }


class ConfigAscendingTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "True"


class ConfigAscendingFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "False"


class ConfigAscending(Config):
    """
    Specifies sorting order: True for ascending (small to large), False for descending (large to small).
    """
    name: Literal["ascending"] = "ascending"
    value: Union[ConfigAscendingTrue, ConfigAscendingFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Ascending"
        json_schema_extra = {
            "shortDescription": "Sort Order Direction"
        }


class SortInputs(Inputs):
    inputDetections: InputDetections


class SortConfigs(Configs):
    sortBy: ConfigSortBy
    ascending: ConfigAscending


class SortOutputs(Outputs):
    outputDetections: OutputDetections


class SortDetectionRequest(Request):
    inputs: SortInputs
    configs: SortConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class SortDetectionResponse(Response):
    outputs: SortOutputs


class SortDetectionExecutor(Config):
    """
    Sorts object detections list by bounding box coordinates, size, or center points.
    """
    name: Literal["SortDetection"] = "SortDetection"
    value: Union[SortDetectionRequest, SortDetectionResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Sort Detection"
        json_schema_extra = {
            "target": {"value": 0},
            "shortDescription": "Sort Detection list"
        }


# --- Package Configurations ---

class ConfigExecutor(Config):
    """
    The primary task execution mode of the component.
    Select 'Detections Filtering' to drop classes, 'Detection Adjustment' to transform bounding boxes, or 'Sort Detection' to order list elements.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[DetectionsFilteringExecutor, DetectionAdjustmentExecutor, SortDetectionExecutor]
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
