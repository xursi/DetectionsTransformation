import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DetectionTransformation.src.models.PackageModel import Detection, PackageModel
from components.DetectionTransformation.src.utils.response import build_adjustment_response


class DetectionAdjustment(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.input_detections = self.request.get_param("inputDetections") or []
        self.target_labels = self._parse_labels(self.request.get_param("targetLabels"))
        self.adjustment_type = self.request.get_param("adjustmentType")

        if self.adjustment_type == "Shift":
            self.shift_x = float(self.request.get_param("shiftX") or 0.0)
            self.shift_y = float(self.request.get_param("shiftY") or 0.0)
        elif self.adjustment_type == "Resize":
            self.scale_width = float(self.request.get_param("scaleWidth") or 1.0)
            self.scale_height = float(self.request.get_param("scaleHeight") or 1.0)

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def _parse_labels(value):
        return {label.strip() for label in str(value or "").split(",") if label.strip()}

    def adjust(self):
        adjusted = []
        for raw_detection in self.input_detections:
            detection = Detection.parse_obj(raw_detection)

            if self.target_labels and detection.classLabel not in self.target_labels:
                adjusted.append(detection.dict())
                continue

            bbox = detection.boundingBox
            if bbox is not None:
                if self.adjustment_type == "Shift":
                    new_left = bbox.left + self.shift_x
                    new_top = bbox.top + self.shift_y
                    bbox.left = max(0.0, new_left)
                    bbox.top = max(0.0, new_top)

                elif self.adjustment_type == "Resize":
                    bbox.width = max(1.0, bbox.width * self.scale_width)
                    bbox.height = max(1.0, bbox.height * self.scale_height)

            adjusted.append(detection.dict())
        return adjusted

    def run(self):
        self.detections = self.adjust()
        return build_adjustment_response(context=self)


if "__main__" == __name__:
    try:
        Executor(sys.argv[1]).run()
    except Exception as e:
        import traceback
        print(f"Executor failed: {e}\n{traceback.format_exc()}", flush=True)
