# Tree Recognition Project

## Data
The dataset is organized within the `Data` folder. Two subsets are present: one with annotations (folder names ending with '7') and another without annotations (folder names ending with '9'). In both cases, bounding box annotations and tree types are included.

To obtain the data:

1. Click on this [link](https://storage.googleapis.com/public-datasets-lila/larch-casebearer/Data_Set_Larch_Casebearer.zip) to download the Larch Dataset.
2. Extract the directory.
3. Open the extracted directory.
4. Copy all the folders (`Ctrl+A`, `Ctrl+C`).
5. Go back to your local repo, create a `Larch_Dataset/` folder.
6. Paste everything into your `Larch_Dataset/` folder.

You should have an architecture like this:
``` 
Larch_Dataset
├── Bebehojd_20190527
├── Bebehojd_20190819
├── Ekbacka_20190527
├── Ekbacka_20190819
├── Jallasvag_20190527
├── Jallasvag_20190819
├── Kampe_20190527
├── Kampe_20190819
├── Nordkap_20190527
└── Nordkap_20190819 
```

From this you can preprocess the data, running `preprocessing.py`. This should create a `Data/` folder et divide the data into 3 parts : **Train**, **Test**, **Validation**. In the same time this script changes the format of the label (or annotation) files from xml to text file but with the YOLO format. You can refer to this [link](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/#21-create-datasetyaml) to know more about the YOLO format


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
