import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DetectionTransformation.src.models.PackageModel import Detection, PackageModel
from components.DetectionTransformation.src.utils.response import build_response


class Filtering(Component):
    def __init__(self, request, bootstrap):
        print("--- Filtering Component Initializing ---", flush=True)
        try:
            super().__init__(request, bootstrap)
            print(f"Request data keys: {list(self.request.data.keys()) if isinstance(self.request.data, dict) else 'not a dict'}", flush=True)
            
            self.request.model = PackageModel(**self.request.data)
            print("PackageModel created successfully", flush=True)

            self.input_detections = self.request.get_param("inputDetections") or []
            print(f"inputDetections loaded: count={len(self.input_detections)}", flush=True)

            self.filter_type = self.request.get_param("filterType")
            print(f"filterType loaded: {self.filter_type}", flush=True)

            raw_allowed = self.request.get_param("allowedLabels")
            self.allowed_labels = self._parse_labels(raw_allowed)
            print(f"allowedLabels loaded: raw='{raw_allowed}', parsed={self.allowed_labels}", flush=True)
            
        except Exception as e:
            print(f"Error in __init__: {e}\n{traceback.format_exc()}", flush=True)
            raise e

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def _parse_labels(value):
        return {label.strip() for label in str(value or "").split(",") if label.strip()}

    def transform(self):
        print("transform() started", flush=True)
        transformed = []
        try:
            for idx, raw_detection in enumerate(self.input_detections):
                print(f"Parsing detection {idx}: {raw_detection}", flush=True)
                detection = Detection.parse_obj(raw_detection)
                print(f"Detection {idx} parsed successfully: label={detection.classLabel}, id={detection.classId}, conf={detection.confidence}", flush=True)

                if self.filter_type == "FilterByLabel" and self.allowed_labels:
                    if detection.classLabel not in self.allowed_labels:
                        print(f"Detection {idx} FILTERED OUT (label '{detection.classLabel}' not in {self.allowed_labels})", flush=True)
                        continue

                transformed.append(detection.dict())
                print(f"Detection {idx} kept", flush=True)
        except Exception as e:
            print(f"Error in transform(): {e}\n{traceback.format_exc()}", flush=True)
            raise e
        print(f"transform() completed, returning {len(transformed)} detections", flush=True)
        return transformed

    def run(self):
        print("run() started", flush=True)
        try:
            self.detections = self.transform()
            response = build_response(context=self)
            print("run() completed successfully", flush=True)
            return response
        except Exception as e:
            print(f"Error in run(): {e}\n{traceback.format_exc()}", flush=True)
            raise e


if __name__ == "__main__":
    print("--- Executor Starting ---", flush=True)
    try:
        Executor(sys.argv[1]).run()
    except Exception as e:
        print(f"Executor failed: {e}\n{traceback.format_exc()}", flush=True)
