import cv2
import xml.etree.ElementTree as ET
from imports import *
from init import *

def load_annotation_from_text(filename):
    
    
    with open(filename, 'r') as file:
        lines = file.readlines()

    annotations = []
    for line in lines:
        data = line.strip().split()
        tree_type = int(data[0])
        center_x, center_y, width, height = map(float, data[1:])
        annotations.append((tree_type, center_x, center_y, width, height))

    return annotations

def load_image(filename):
    
    image = cv2.imread(filename)
    return image


def define_colors(tree_type):
    if tree_type == 0:
        return (255, 0, 255), (0, 0, 0)  # Red for other tree types
    elif tree_type == 1:
        return (0, 255, 0), (0, 0, 0)  # Green for Healthy (overrides tree type color)
    elif tree_type == 2:
        return (0, 255, 255), (0, 0, 0)  # Darker Red for High Damage
    elif tree_type == 3:
        return (0, 0, 255), (0, 0, 0)  # Darker Red for High Damage

def draw_bbox(image, bbox, rect_color, text_color, text):
    center_x, center_y, width, height = bbox

    # Calculate top-left and bottom-right coordinates from center, width, and height
    image_original_size = 640
    xmin = int((center_x - width / 2)*image_original_size)
    ymin = int((center_y - height / 2)*image_original_size)
    xmax = int((center_x + width / 2)*image_original_size)
    ymax = int((center_y + height / 2)*image_original_size)


    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), rect_color, 2)

    # Get the size of the text
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    print(f"Text Position: ({xmin}, {ymin - text_height - 5}) to ({xmin + text_width}, {ymin})")

    # Draw a filled rectangle as a background for text
    cv2.rectangle(image, (xmin, ymin - text_height - 5), (xmin + text_width, ymin), rect_color, -1)

    # Display tree type information with the same color
    cv2.putText(image, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
    

    return image


def annotate_image_from_text(annotation_file, image_file, image_annotated_file,int_to_labels):
    annotations = load_annotation_from_text(annotation_file)
    image = load_image(image_file)

    for annotation in annotations:
        tree_type, center_x, center_y, width, height = annotation
        rect_color, text_color = define_colors(tree_type)
        text = int_to_labels[tree_type]
        draw_bbox(image, annotation[1:], rect_color, text_color, text)

    # Save the annotated image
    cv2.imwrite(image_annotated_file, image)


folder_name = "Data/train/"
image_file = folder_name + "images/B02_0051270.JPG"
label_file = folder_name + "labels/B02_0051270.txt"
image_annotated_file = "Test/B02_0051270_annoatated.JPG"

annotate_image_from_text(label_file,image_file,image_annotated_file,int_to_labels)