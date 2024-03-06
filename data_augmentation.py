import os
from imports import *
from init import *

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
        print(trees_amount, proportions)
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
        print(file_name)
        
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

def plot_kept_stat(folder_list,labels_folder, int_to_labels, labels_to_int):

    amount_trees = {}
    for filename in folder_list:
        amount_trees_img, _ = calculate_tree_stats(filename,labels_folder,int_to_labels,labels_to_int)
        amount_trees = add_values(amount_trees,amount_trees_img)
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


def keep_H(proportions_per_image):
    images_to_increase = []
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
            images_to_increase.append(image_name)
    
    return images_to_increase

def rotate_image(input_path, output_path,rotation):
    # Open the image file
    with Image.open(input_path) as img:
        # Rotate the image 90 degrees clockwise
        rotated_img = img.rotate(rotation, expand=True)

        # Save the rotated image to the specified output path
        rotated_img.save(output_path)

def rotate_boxes(input_boxes_path, output_boxes_path,rotation):
    # Read the box data from the file
    with open(input_boxes_path, 'r') as box_file:
        box_lines = box_file.readlines()

    # Rotate and save the rotated bounding boxes
    with open(output_boxes_path, 'w') as output_box_file:
        for box_line in box_lines:
            # Parse box coordinates
            box_data = box_line.strip().split()
            box_class = int(box_data[0])
            x, y, width, height = map(float, box_data[1:])
            if rotation == 90:
                rotated_x = y  # Swap x and y
                rotated_y = 1 - x  # Adjust y
                rotated_width = height
                rotated_height = width
            elif rotation == 180:
                rotated_x = 1 - x  # Swap x and y
                rotated_y = 1 - y   # Adjust y
                rotated_width = width
                rotated_height = height
            elif rotation == 270:
                rotated_x = 1 - y  # Swap x and y
                rotated_y = x  # Adjust y
                rotated_width = height
                rotated_height = width

            # Save the rotated box data to the output file
            output_box_file.write(f"{box_class} {rotated_x:.6f} {rotated_y:.6f} {rotated_width:.6f} {rotated_height:.6f}\n")


def rotate_data(labels_list,folder_name):
    for labels in labels_list:
        root = labels.split(".")[0]
        img_type = "images/"
        label_type = "labels/"
        label_ext = ".txt"
        img_ext = ".JPG"
        rotation_base = 90
        # Rotate the image three times
        for i in range(1,4):
            rotation = i*rotation_base
            print(i)
            print(rotation)
            label_file = folder_name + label_type + root + label_ext
            image_file = folder_name + img_type + root + img_ext
            output_label_file= folder_name+ label_type + root + str(rotation) + label_ext
            output_image_file= folder_name + img_type + root + str(rotation) + img_ext
            rotate_image(image_file,output_image_file,rotation)
            rotate_boxes(label_file,output_label_file,rotation)




train_labels_folder = 'Data/train/labels/'
val_labels_folder = 'Data/valid/labels/'
filename = "B01_0004.txt"

trees_amount,proportions = calculate_tree_stats(filename,train_labels_folder, int_to_labels,labels_to_int)

# print(trees_amount)
# print(proportions)

plot_stat(train_labels_folder,int_to_labels,labels_to_int)
sum,train_proportion_per_images = get_proportions_per_image(train_labels_folder, int_to_labels,labels_to_int)
# proportions_par_image_valid = get_proportions_per_image(val_labels_folder, int_to_labels)
print(train_proportion_per_images)

augmented_images_train = keep_H(train_proportion_per_images)


plot_kept_stat(augmented_images_train,train_labels_folder,int_to_labels,labels_to_int)
plot_stat(train_labels_folder,int_to_labels,labels_to_int)


folder_name = "Data/train/"
rotate_data(augmented_images_train,folder_name)
plot_stat(train_labels_folder,int_to_labels,labels_to_int)