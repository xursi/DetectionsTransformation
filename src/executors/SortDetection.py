import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DetectionTransformation.src.models.PackageModel import Detection, PackageModel
from components.DetectionTransformation.src.utils.response import build_sort_response


class SortDetection(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.input_detections = self.request.get_param("inputDetections") or []
        
        # Retrieve configuration options and normalize their values
        raw_sort_by = self.request.get_param("sortBy")
        self.sort_by = raw_sort_by.value if hasattr(raw_sort_by, "value") else str(raw_sort_by or "x_min")
        
        raw_ascending = self.request.get_param("ascending")
        if hasattr(raw_ascending, "value"):
            self.ascending = bool(raw_ascending.value)
        else:
            self.ascending = str(raw_ascending).lower() != "false"

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def transform(self):
        parsed_detections = []
        for raw_detection in self.input_detections:
            parsed_detections.append(Detection.parse_obj(raw_detection))

        def get_sort_key(detection):
            if self.sort_by == "confidence":
                return detection.confidence
            
            bbox = detection.boundingBox
            if self.sort_by == "x_min":
                return bbox.left
            elif self.sort_by == "x_max":
                return bbox.left + bbox.width
            elif self.sort_by == "y_min":
                return bbox.top
            elif self.sort_by == "y_max":
                return bbox.top + bbox.height
            elif self.sort_by == "size":
                return bbox.width * bbox.height
            elif self.sort_by == "center_x":
                return bbox.left + (bbox.width / 2.0)
            elif self.sort_by == "center_y":
                return bbox.top + (bbox.height / 2.0)
            return 0.0

        # Sort the detections list
        # reverse=True in python sorted() does descending sort.
        # Since ascending=True means small-to-large, we set reverse=not self.ascending.
        sorted_detections = sorted(parsed_detections, key=get_sort_key, reverse=not self.ascending)
        
        return [d.dict() for d in sorted_detections]

    def run(self):
        self.detections = self.transform()
        return build_sort_response(context=self)


if __name__ == "__main__":
    try:
        Executor(sys.argv[1]).run()
    except Exception as e:
        import traceback
        print(f"Executor failed: {e}\n{traceback.format_exc()}", flush=True)
