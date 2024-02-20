# Tree Recognition Project

## Data
The dataset is organized within the `data` folder. Two subsets are present: one with annotations (folder names ending with '7') and another without annotations (folder names ending with '9'). In both cases, bounding box annotations and tree types are included.

### Annotations
For the annotated subset:
- **Bounding Box Annotations:** Present for all images.
- **Damage Annotations:**
  - **H:** Healthy
  - **LD:** Light Damage
  - **HD:** High Damage
  - **Other:** Unspecified

### Tree Types
The tree type is also annotated:
- **Larch:** Pertaining to the trees of interest.
- **Other:** Denoting trees that are not relevant to the project.

## Test 
The `test` folder contains two scripts:
1. `draw_annotations.py`: A script to visualize bounding box annotations on an image.
2. `yolo_webcam_test.py`: A test script demonstrating YOLO object detection using a webcam.

Feel free to explore and use these scripts for testing and visualization purposes.
