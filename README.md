# Detection Transformation

NovaVision component that filters YOLO detections by confidence and class labels,
and can rename one class label. Bounding-box, class ID, keypoints, and image UID
are preserved in the output.

## Settings

- **Minimum confidence:** Keep detections at or above this score (`0` disables it).
- **Maximum confidence:** Keep detections at or below this score (`1` disables it).
- **Allowed labels:** Comma-separated labels to keep; leave empty to keep all.
- **Rename source label / target label:** Rename only when both fields are set.
