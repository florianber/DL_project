TRAIN = True
# Number of epochs to train for.
EPOCHS = 25
int_to_labels = {0:"Other",1: "Larch-H", 2: "Larch-LD", 3: "Larch-HD"}
labels_to_int = {"Other": 0, "Larch-H": 1, "Larch-LD": 2, "Larch-HD": 3}
CLASSIC_ROOT_LEN = len("B01_0004.txt".split()[0])
ROTATIONS = [90, 180, 270]
MIRROR = ["x","y"]
IMG_FOLDER = "images/"
LABEL_FOLDER = "labels/"
TXT_EXT = ".txt"
IMG_EXT = ".JPG"
TRAIN_FOLDER = "train/"
TEST_FOLDER = "test/"
VAL_FOLDER = "val/"
