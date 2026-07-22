# Detection Transformation

NovaVision component for applying exactly one transformation to YOLO detections.
The first available task is filtering by class label. Bounding-box, confidence,
class ID, keypoints, and image UID are preserved in the output.

## Settings

- **Task:** Select `Filtering`.
- **Filter type:** Select `By Label`.
- **Allowed labels:** Comma-separated labels to keep; leave empty to keep all.

Future tasks, such as label renaming and filtering by position or bounding-box
area, can be added as separate options under **Task** or **Filter type**.
