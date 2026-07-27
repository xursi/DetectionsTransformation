import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DetectionTransformation.src.models.PackageModel import Detection, PackageModel
from components.DetectionTransformation.src.utils.response import build_response


class Filtering(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.input_detections = self.request.get_param("inputDetections") or []
        self.filter_type = self.request.get_param("filterType")
        self.allowed_labels = self._parse_labels(self.request.get_param("allowedLabels"))

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def _parse_labels(value):
        print(f"Parsing allowed labels: {value}")
        return {label.strip() for label in str(value or "").split(",") if label.strip()}

    def transform(self):
        transformed = []
        for raw_detection in self.input_detections:
            detection = Detection.parse_obj(raw_detection)

            print(f"Processing detection: {detection.classLabel}")
            if self.filter_type == "FilterByLabel"  and self.allowed_labels and detection.classLabel not in self.allowed_labels:
                continue

            transformed.append(detection.dict())
        return transformed

    def run(self):
        self.detections = self.transform()
        return build_response(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
