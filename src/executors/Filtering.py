import os
import sys
import traceback
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DetectionTransformation.src.models.PackageModel import Detection, PackageModel
from components.DetectionTransformation.src.utils.response import build_response


def log_debug(msg):
    try:
        # Docker'da /storage mount edilmiştir, yoksa local dizine yazar
        path = "/storage/debug.log" if os.path.exists("/storage") else "debug.log"
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception as e:
        sys.stderr.write(f"Log yazma hatası: {e}\n")


class Filtering(Component):
    def __init__(self, request, bootstrap):
        log_debug("--- Filtering Component Initializing ---")
        try:
            super().__init__(request, bootstrap)
            log_debug(f"Request data keys: {list(self.request.data.keys()) if isinstance(self.request.data, dict) else 'not a dict'}")
            
            self.request.model = PackageModel(**self.request.data)
            log_debug("PackageModel created successfully")

            self.input_detections = self.request.get_param("inputDetections") or []
            log_debug(f"inputDetections loaded: count={len(self.input_detections)}")

            self.filter_type = self.request.get_param("filterType")
            log_debug(f"filterType loaded: {self.filter_type}")

            raw_allowed = self.request.get_param("allowedLabels")
            self.allowed_labels = self._parse_labels(raw_allowed)
            log_debug(f"allowedLabels loaded: raw='{raw_allowed}', parsed={self.allowed_labels}")
            
        except Exception as e:
            log_debug(f"Error in __init__: {e}\n{traceback.format_exc()}")
            raise e

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def _parse_labels(value):
        return {label.strip() for label in str(value or "").split(",") if label.strip()}

    def transform(self):
        log_debug("transform() started")
        transformed = []
        try:
            for idx, raw_detection in enumerate(self.input_detections):
                log_debug(f"Parsing detection {idx}: {raw_detection}")
                detection = Detection.parse_obj(raw_detection)
                log_debug(f"Detection {idx} parsed successfully: label={detection.classLabel}, id={detection.classId}, conf={detection.confidence}")

                if self.filter_type == "FilterByLabel" and self.allowed_labels:
                    if detection.classLabel not in self.allowed_labels:
                        log_debug(f"Detection {idx} FILTERED OUT (label '{detection.classLabel}' not in {self.allowed_labels})")
                        continue

                transformed.append(detection.dict())
                log_debug(f"Detection {idx} kept")
        except Exception as e:
            log_debug(f"Error in transform(): {e}\n{traceback.format_exc()}")
            raise e
        log_debug(f"transform() completed, returning {len(transformed)} detections")
        return transformed

    def run(self):
        log_debug("run() started")
        try:
            self.detections = self.transform()
            response = build_response(context=self)
            log_debug("run() completed successfully")
            return response
        except Exception as e:
            log_debug(f"Error in run(): {e}\n{traceback.format_exc()}")
            raise e


if __name__ == "__main__":
    log_debug("--- Executor Starting ---")
    try:
        Executor(sys.argv[1]).run()
    except Exception as e:
        log_debug(f"Executor failed: {e}\n{traceback.format_exc()}")
