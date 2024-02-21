from imports import *
from datamodule import *
from init import labels_to_int ,int_to_labels

# For converting XML annotations to YOLO format for a single image

def convert_xml_to_YOLOformat(source, destination,labels_to_int):
    """
    Converts XML annotations to YOLO format for a single image.

    Parameters:
    - source (str): Path to the source XML file.
    - destination (str): Path to the destination TXT file (YOLO format).

    Returns:
    None
    """
    tree = ET.parse(source)
    root = tree.getroot()

    # Get image size
    image_size = root.find("size")
    image_width = int(image_size.find("width").text)
    image_height = int(image_size.find("height").text)

    # Open a TXT file for writing
    txt_filename = destination
    with open(txt_filename, 'w') as txtfile:
        # Extract data and write lines
        for obj in root.findall("object"):
            tree_type = obj.find("tree").text
            damage = obj.find("damage").text
            bndbox = obj.find("bndbox")
            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)

            # Convert coordinates to YOLO format with normalization
            x_center = (xmin + xmax) / 2.0 / image_width
            y_center = (ymin + ymax) / 2.0 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height

            # Format the line based on tree type and damage
            if tree_type == "Other":
                label = labels_to_int[tree_type]
                line = f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            else:
                label = labels_to_int[f"{tree_type}-{damage}"]
                line = f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            txtfile.write(line)

    print(f"TXT file '{txt_filename}' has been created.")

def clean_and_preprocess_data(source, train_dir, test_dir, val_dir, split_ratio=(0.8, 0.1, 0.1)):
    """
    Cleans and preprocesses data by splitting them into training, testing, and validation sets.
    Converts XML annotations to YOLO format for each image.
    
    Parameters:
    - source (str): Path to the source directory.
    - train_dir (str): Path to the training set directory.
    - test_dir (str): Path to the testing set directory.
    - val_dir (str): Path to the validation set directory.
    - split_ratio (tuple): Split ratios for training, testing, and validation.

    Returns:
    None
    """
    text_extension = ".txt"
    images_dir = "images"
    labels_dir = "labels"
    directory_to_create = [train_dir, test_dir, val_dir]

    for directory in directory_to_create:
        create_directory(f"{directory}/{images_dir}/")
        create_directory(f"{directory}/{labels_dir}/")

    # Iterate through the source directories
    for category in sorted(os.listdir(source)):
        annotation_files, image_files, annotation_path, image_path = get_files_and_path(source, category, directory_to_create)

        if annotation_files == 0:
            continue

        gathered_list = gather_image_annotation(annotation_files, image_files)
        shuffled_list = random.sample(gathered_list, len(gathered_list))
        train_split, test_split = split_spot(gathered_list=gathered_list, split_ratio=split_ratio)

        # Move files to respective directories
        for i, anot_imag in enumerate(shuffled_list):
            try:
                root = anot_imag[0].split(".")[0]
                src_path_annotation, src_path_image = create_src_path(anot_imag, annotation_path, image_path)
                print(src_path_annotation)
                dest_path = (
                    train_dir if i < train_split else test_dir if i < test_split else val_dir
                )
                convert_xml_to_YOLOformat(source=src_path_annotation, destination=f"{dest_path}/{labels_dir}/{root}{text_extension}",labels_to_int=labels_to_int)
                shutil.copy(src_path_image, f"{dest_path}/{images_dir}")
            except Exception as e:
                print(f"Error {e}")

if __name__ == "__main__":
    source_directory = "Larch_Dataset"
    destination_directory = "Data"
    train_directory = f"{destination_directory}/train"
    test_directory = f"{destination_directory}/test"
    val_directory = f"{destination_directory}/valid"

    clean_and_preprocess_data(source_directory, train_directory, test_directory, val_directory)
