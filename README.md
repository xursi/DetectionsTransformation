# Detections Transformation Component

A highly modular computer vision post-processing component designed for the **NovaVision Suite**. This component intercepts object detection metadata (such as bounding boxes and class labels) downstream from inference models (like YOLO) to filter, adjust, or reorder the detections list in real time.

---

## 🚀 Key Features (Tasks)

The component operates in three distinct execution modes, selectable via the **Task** dropdown in the visual editor:

### 1. Detections Filtering
Filters the incoming list of detections, keeping only the objects of interest.
*   **Allowed Labels (`allowedLabels`)**: A comma-separated list of target labels (e.g., `person, car, cup`). Only detections matching these classes are passed to output. If left empty, all detections are kept.

### 2. Detection Adjustment
Performs geometric modifications (translation and scaling) to bounding box coordinates for specific classes.
*   **Target Labels (`targetLabels`)**: Specifies which classes undergo transformation. If empty, all boxes are transformed.
*   **Adjustment Type (`adjustmentType`)**:
    *   **Shift**: Translates bounding box positions by a pixel offset (`shiftX` and `shiftY`).
    *   **Resize**: Scales bounding box dimensions using width/height multipliers (`scaleWidth` and `scaleHeight`).
*   *Safety Feature*: Includes native coordinate clamping (`left >= 0.0`, `top >= 0.0`, `width >= 1.0`, `height >= 1.0`) to prevent bounding boxes from sliding outside frame bounds or shrinking to zero.

### 3. Sort Detection
Reorders the detection sequence according to spatial position, size, or confidence.
*   **Sort By (`sortBy`)**: Selects the target attribute to sort on:
    *   `x_min` / `x_max` / `y_min` / `y_max` (box coordinate boundaries)
    *   `center_x` / `center_y` (box center coordinates)
    *   `size` (bounding box area: width * height)
    *   `confidence` (detection confidence score)
*   **Ascending (`ascending`)**: Direction of sorting. `True` sorts from smallest to largest; `False` sorts from largest to smallest.

---

## 🛠️ Architecture & Directory Layout

The package complies with NovaVision's component structure:

```text
DetectionsTransformation/
├── src/
│   ├── models/
│   │   └── PackageModel.py      # Pydantic schemas, UI form definitions, tooltips
│   ├── utils/
│   │   └── response.py          # Output formatting & packaging helpers
│   └── executors/
│       ├── DetectionsFiltering.py  # Logic for class label filtering
│       ├── DetectionAdjustment.py # Logic for box shifting and scaling
│       └── SortDetection.py       # Logic for sorting list elements
└── README.md
```

1.  **UI/Schema Layer (`models/PackageModel.py`)**: Uses Pydantic to declare parameters, dropdown structures, default values, and tooltips. The system compiles these schemas to dynamically render input forms in the web UI.
2.  **Business Logic Layer (`executors/`)**: Separate Python scripts containing specific algorithms for each task. The system triggers the corresponding executor script based on the selected task.
3.  **Packaging Layer (`utils/response.py`)**: Wraps output data into the strict JSON formats required by the pipeline.

---

## ⚙️ How It Works (Technical Execution Flow)

1.  **Inference Data Input**: The component accepts a list of detections (`List[Detection]`) via the `inputDetections` socket.
2.  **Configuration Parsing**: The active executor parses the selected task, sub-options, and variables from the UI payload.
3.  **Transformation Algorithm**:
    *   *Filtering*: Performs set lookup against `allowedLabels`.
    *   *Adjustment*: Modifies box coordinates `left`, `top`, `width`, and `height` while clamping to positive values.
    *   *Sorting*: Sorts the array using Python's optimized `sorted()` function with a custom lambda key mapper.
4.  **Result Output**: Emits the modified detection list through the `outputDetections` socket to visualization, counting, or tracking nodes.
