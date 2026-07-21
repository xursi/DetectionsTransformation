import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from src.models.PackageModel import Detection, PackageModel
from src.utils.response import build_response


class DetectionTransformation(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.input_detections = self.request.get_param("inputDetections")
        self.min_confidence = float(self.request.get_param("minConfidence"))
        self.max_confidence = float(self.request.get_param("maxConfidence"))
        self.allowed_labels = self._parse_labels(self.request.get_param("allowedLabels"))
        self.rename_source = str(self.request.get_param("renameSourceLabel") or "").strip()
        self.rename_target = str(self.request.get_param("renameTargetLabel") or "").strip()

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def _parse_labels(value):
        return {label.strip() for label in str(value or "").split(",") if label.strip()}

    def transform(self):
        transformed = []
        for raw_detection in self.input_detections:
            detection = Detection.parse_obj(raw_detection)

            if not self.min_confidence <= detection.confidence <= self.max_confidence:
                continue
            if self.allowed_labels and detection.classLabel not in self.allowed_labels:
                continue
            if self.rename_source and self.rename_target and detection.classLabel == self.rename_source:
                detection.classLabel = self.rename_target

            transformed.append(detection.dict())
        return transformed

    def run(self):
        self.detections = self.transform()
        return build_response(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
