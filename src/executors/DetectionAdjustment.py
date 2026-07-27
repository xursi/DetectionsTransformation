import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DetectionTransformation.src.models.PackageModel import Detection, PackageModel
from components.DetectionTransformation.src.utils.response import build_adjustment_response


class DetectionAdjustment(Component):
    def __init__(self, request, bootstrap):
        print("--- DetectionAdjustment Component Initializing ---", flush=True)
        try:
            super().__init__(request, bootstrap)
            self.request.model = PackageModel(**self.request.data)
            print("PackageModel created successfully", flush=True)

            self.input_detections = self.request.get_param("inputDetections") or []
            print(f"inputDetections loaded: count={len(self.input_detections)}", flush=True)

            self.target_labels = self._parse_labels(self.request.get_param("targetLabels"))
            print(f"targetLabels loaded: {self.target_labels}", flush=True)

            self.adjustment_type = self.request.get_param("adjustmentType")
            print(f"adjustmentType loaded: {self.adjustment_type}", flush=True)

            if self.adjustment_type == "Shift":
                self.shift_x = float(self.request.get_param("shiftX") or 0.0)
                self.shift_y = float(self.request.get_param("shiftY") or 0.0)
                print(f"Shift parameters: X={self.shift_x}, Y={self.shift_y}", flush=True)
            elif self.adjustment_type == "Resize":
                self.scale_width = float(self.request.get_param("scaleWidth") or 1.0)
                self.scale_height = float(self.request.get_param("scaleHeight") or 1.0)
                print(f"Scale parameters: Width={self.scale_width}, Height={self.scale_height}", flush=True)

        except Exception as e:
            print(f"Error in __init__: {e}\n{traceback.format_exc()}", flush=True)
            raise e

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def _parse_labels(value):
        return {label.strip() for label in str(value or "").split(",") if label.strip()}

    def adjust(self):
        print("adjust() started", flush=True)
        adjusted = []
        try:
            for idx, raw_detection in enumerate(self.input_detections):
                detection = Detection.parse_obj(raw_detection)

                # Target label filter check: if targetLabels is not empty, check if detection is in targetLabels
                if self.target_labels and detection.classLabel not in self.target_labels:
                    # Skip transformation for this label, append as is
                    adjusted.append(detection.dict())
                    continue

                bbox = detection.boundingBox
                if bbox is not None:
                    if self.adjustment_type == "Shift":
                        # Apply shiftX / shiftY to left / top
                        new_left = bbox.left + self.shift_x
                        new_top = bbox.top + self.shift_y
                        
                        # Boundary check: left and top cannot be negative
                        bbox.left = max(0.0, new_left)
                        bbox.top = max(0.0, new_top)
                        print(f"Detection {idx} shifted: left={bbox.left}, top={bbox.top}", flush=True)

                    elif self.adjustment_type == "Resize":
                        # Apply scaleWidth / scaleHeight to width / height.
                        # Keep width and height at least 1.0
                        bbox.width = max(1.0, bbox.width * self.scale_width)
                        bbox.height = max(1.0, bbox.height * self.scale_height)
                        print(f"Detection {idx} resized: width={bbox.width}, height={bbox.height}", flush=True)

                adjusted.append(detection.dict())
        except Exception as e:
            print(f"Error in adjust(): {e}\n{traceback.format_exc()}", flush=True)
            raise e
        print(f"adjust() completed, returning {len(adjusted)} detections", flush=True)
        return adjusted

    def run(self):
        print("run() started", flush=True)
        try:
            self.detections = self.adjust()
            response = build_adjustment_response(context=self)
            print("run() completed successfully", flush=True)
            return response
        except Exception as e:
            print(f"Error in run(): {e}\n{traceback.format_exc()}", flush=True)
            raise e


if "__main__" == __name__:
    print("--- Adjustment Executor Starting ---", flush=True)
    try:
        Executor(sys.argv[1]).run()
    except Exception as e:
        print(f"Executor failed: {e}\n{traceback.format_exc()}", flush=True)
