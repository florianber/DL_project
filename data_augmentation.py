import os
from imports import *
from init import *
from datamodule import create_directory

def read_text_file(file_path, labels_folder):
    with open(labels_folder + file_path, 'r') as file:
        lines = file.readlines()
        # Assuming each line in the file corresponds to an annotation
        annotations = [line.strip().split() for line in lines]
    return annotations

# Calculate the proportion of each tree type in a photo based on labels
def calculate_tree_stats(filename, labels_folder, int_to_labels, labels_to_int):
    trees_amount = {label: 0 for label in int_to_labels.values()}
    annotations = read_text_file(filename, labels_folder)
    if len(annotations) != 0:
        trees_sum = len(annotations)
        for annotation in annotations:
            # The first column represents the tree type
            tree_type = int(annotation[0])
            label = int_to_labels[tree_type]
            trees_amount[label] += 1

        # Calculate proportions
        proportions = {label: count / trees_sum for label, count in trees_amount.items()}
        return trees_amount, proportions
    else:
        for key,value in labels_to_int.items():
            labels_to_int[key] = 0
        return labels_to_int, labels_to_int

def add_values(sum_dictionary, file_dictionary):
    for key, value in file_dictionary.items():
        if key in sum_dictionary:
            # If the key already exists, add the new value to the existing value
            sum_dictionary[key] += value
        else:
            # If the key doesn't exist, create a new entry
            sum_dictionary[key] = value

    return sum_dictionary

def get_proportions_per_image(labels_folder, int_to_labels, labels_to_int):
    proportions_per_image = {}
    count_per_class = {}

    # List of file names in the folder
    file_names = os.listdir(labels_folder)

    for file_name in file_names:
              
        count_file,proportions_file = calculate_tree_stats(file_name, labels_folder, int_to_labels, labels_to_int)

        # Add the proportions of this file to the list
        sum_dictionary = add_values(count_per_class, count_file)
        proportions_per_image[file_name] = proportions_file

    return sum_dictionary, proportions_per_image

# Display proportions for each image
def plot_stat(folder_name, int_to_labels, labels_to_int):

    amount_trees, _ = get_proportions_per_image(folder_name, int_to_labels, labels_to_int)
    categories = list(amount_trees.keys())
    values = list(amount_trees.values())

    # Colors available
    colors = ['blue', 'green', 'orange', 'red']

    # Create a bar plot
    plt.bar(categories, values, color=colors)

    # Add labels and title
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Plot from Dictionary')

    # Show the plot
    plt.show()

def make_dict_sum(dict):
    return sum(dict.values())




def data_kept(proportions_per_image):
    images_to_rotate = []
    dict_sum = {}
    for image_name, proportions in proportions_per_image.items():
        proportion_H = proportions.get("Larch-H", 0)
        proportion_LD = proportions.get("Larch-LD", 0)
   
        # Add the image name to the list if the proportion of H or HD is greater than 30%
        if proportion_H > proportion_LD:
            print(f"{image_name}:")
            for label, proportion in proportions.items():
                print(f"   {label}: {proportion * 100:.2f}%")
            dict_sum = add_values(dict_sum,proportions)
            images_to_rotate.append(image_name)
    
    return images_to_rotate

def rotate_image(input_file):
    # Open the image file
    with Image.open(input_file) as img:
        # Rotate the image 90 degrees clockwise
        for rotation in ROTATIONS:
            print(input_file.split(".")[0])
            rotated_file = input_file.split(".")[0] +f"_{rotation}{IMG_EXT}"
            rotated_img = img.rotate(rotation, expand=True)
            rotated_img.save(rotated_file)

def rotate_boxes(input_file):

    # Read the box data from the file
    with open(input_file, 'r') as box_file:
        box_lines = box_file.readlines()

    # Rotate and save the rotated bounding boxes for each rotation
    for rotation in ROTATIONS:
        rotated_file = input_file.split(".")[0] + f"_{rotation}{TXT_EXT}"
        with open(rotated_file, 'w') as output_box_file:
            for box_line in box_lines:
                # Parse box coordinates
                box_data = box_line.strip().split()
                box_class = int(box_data[0])
                x, y, width, height = map(float, box_data[1:])
                # Perform rotation based on the specified angle
                if rotation == 90:
                    rotated_x = y
                    rotated_y = 1 - x
                    rotated_width = height
                    rotated_height = width
                elif rotation == 180:
                    rotated_x = 1 - x
                    rotated_y = 1 - y
                    rotated_width = width
                    rotated_height = height
                elif rotation == 270:
                    rotated_x = 1 - y
                    rotated_y = x
                    rotated_width = height
                    rotated_height = width

                # Save the rotated box data to the output file
                output_box_file.write(f"{box_class} {rotated_x:.6f} {rotated_y:.6f} {rotated_width:.6f} {rotated_height:.6f}\n")

def mirror_image(input_file):
    # Open the image file
    for mirror in MIRROR:
        with Image.open(input_file) as img:
            # Apply mirror transformation
            if mirror == "x":
                mirrored_file = input_file.split(".")[0] + "_mirrored_"+mirror + IMG_EXT
                mirrored_img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
                mirrored_img.save(mirrored_file)
            elif mirror == "y":
                mirrored_file = input_file.split(".")[0] + "_mirrored_"+mirror + IMG_EXT
                mirrored_img = img.transpose(method=Image.FLIP_TOP_BOTTOM)
                mirrored_img.save(mirrored_file)

def mirror_boxes(input_file):
    # Read the box data from the file
    with open(input_file, 'r') as box_file:
        box_lines = box_file.readlines()

    # Apply mirror transformation to the bounding boxes
    for mirror in MIRROR:
        print(input_file.split("."))
        mirrored_file = input_file.split(".")[0] + "_mirrored_"+mirror + TXT_EXT

        with open(mirrored_file, 'w') as output_box_file:
            for box_line in box_lines:
                # Parse box coordinates
                box_data = box_line.strip().split()
                box_class = int(box_data[0])
                x, y, width, height = map(float, box_data[1:])
                
                if mirror == "x":
                # Apply mirror transformation to the box coordinates
                    mirrored_x = 1 - x
                    mirrored_y = y
                    mirrored_width = width
                    mirrored_height = height
                elif mirror == "y":
                # Apply mirror transformation to the box coordinates
                    mirrored_x = x
                    mirrored_y = 1 - y
                    mirrored_width = width
                    mirrored_height = height

                # Save the mirrored box data to the output file
                output_box_file.write(f"{box_class} {mirrored_x:.6f} {mirrored_y:.6f} {mirrored_width:.6f} {mirrored_height:.6f}\n")






def apply_data_aug(labels_list,data_folder,data_augm_folder):
    shutil.rmtree(data_augm_folder)
    shutil.copytree(data_folder,data_augm_folder)
    folder_name = data_augm_folder + TRAIN_FOLDER
    for labels in labels_list:
        root = labels.split(".")[0]
        label_file = folder_name + LABEL_FOLDER + root + TXT_EXT
        image_file = folder_name + IMG_FOLDER + root + IMG_EXT
        rotate_image(image_file)
        rotate_boxes(label_file)
        mirror_image(image_file)
        mirror_boxes(label_file)

def main(data_aug):
    
    train_labels_folder = 'Data/train/labels/'
    data_folder= "Data/"
    data_augm_folder = "DataAugmentation/"
    train_labels_augm_folder = "DataAugmentation/train/labels/"

    if data_aug:
        # First plot to the distribution
        plot_stat(train_labels_folder,int_to_labels,labels_to_int)
        sum,train_proportion_per_images = get_proportions_per_image(train_labels_folder, int_to_labels,labels_to_int)
        total_trees = make_dict_sum(sum)
        # Show the initial amount of trees
        print(total_trees)

        augmented_images_train = data_kept(train_proportion_per_images)
        apply_data_aug(augmented_images_train,data_folder,data_augm_folder)
        
        sum,train_proportion_per_images = get_proportions_per_image(train_labels_augm_folder, int_to_labels,labels_to_int)
        total_trees = make_dict_sum(sum)
        print(total_trees)
        plot_stat(train_labels_augm_folder,int_to_labels,labels_to_int)

    else:
        sum,train_proportion_per_images = get_proportions_per_image(train_labels_folder, int_to_labels,labels_to_int)
        total_trees = make_dict_sum(sum)
        print(f"Amount of trees in Data: {total_trees}")
        print(f"Proportions of trees in Data: {sum}")
        plot_stat(train_labels_folder,int_to_labels,labels_to_int)
        sum,train_proportion_per_images = get_proportions_per_image(train_labels_augm_folder, int_to_labels,labels_to_int)
        total_trees = make_dict_sum(sum)
        print(f"Amount of trees in DataAugmentation: {total_trees}")
        print(f"Proportions of trees in Data: {sum}")
        plot_stat(train_labels_augm_folder,int_to_labels,labels_to_int)

if __name__ == "__main__":
    main(data_aug=True)


