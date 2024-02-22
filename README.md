# Tree Recognition Project

## Data
The dataset is organized within the `Larch_Daset` folder. Two subsets are present: one with annotations (folder names ending with '7') and another without annotations (folder names ending with '9'). In both cases, bounding box annotations and tree types are included. Unfortunately, this dataset cannot be pushed on git because of its size 3.6 GB, so the following part is about this. However the dataset used for training is on the git in the `Data` so you should not need to do the following step anymore. If so go on the train tab.

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

From this point on, you can preprocess the data by running preprocessing.py. This script will create a `Data/` folder and divide the data into three parts: **Train**, **Test**, and **Validation**. Simultaneously, the script transforms the label files from XML to text files using the YOLO format, and resize the images to the YOLO format as well which is (640,640). For more information about the YOLO format, refer to this [link](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/#21-create-datasetyaml).

Upon completing this step, you should still have your original `Larch_Dataset/` alongside the newly created `Data/`. If desired, you can remove the `Larch_Dataset/` directory to free up space. Your `Data/` directory should have the following structure:


```
Data
├── test
│   ├── images
│   └── labels
├── train
│   ├── images
│   └── labels
└── valid
    ├── images
    └── labels
```
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


## Train the model

Before to train you need to import the yolov5 repository. You need to be in your project repo and clone the yolov5 repo with this command:
**`git clone git@github.com:ultralytics/yolov5.git`**

From here you can try to train the model. I provide here an example of command to pass through the terminal but you can change every parameter you want following the ones in the `train.py` file of the yolov5 repo. Also you need to be in your repo in the yolov5 repo to execute the following command:
`python train.py --data ../data.yaml --weights yolov5n.pt --img 640 --epochs 10 --batch-size 16`

You can change the batch size to 8 if you are struggling running the training. You can also increase or decrease the amount of epochs.

All the results  will be in the `yolov5/run/train/` in the last exp folder.


