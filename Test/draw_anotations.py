import cv2
import xml.etree.ElementTree as ET

# Load XML annotation

FILE = "B01_0007"
xml_file = f"Larch_Dataset/Bebehojd_20190527/Annotations/{FILE}.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Load image
image_path = f"Larch_Dataset/Bebehojd_20190527/Images/{FILE}.JPG"
image = cv2.imread(image_path)

for obj in root.findall("object"):
    tree_type = obj.find("tree").text
    damage = obj.find("damage").text
    bbox = obj.find("bndbox")
    
    xmin = int(bbox.find("xmin").text)
    ymin = int(bbox.find("ymin").text)
    xmax = int(bbox.find("xmax").text)
    ymax = int(bbox.find("ymax").text)

    # Define color based on tree type and damage
    if tree_type == 'Larch':
        if damage == 'H':
            rect_color = (0, 255, 0)  # Green for Healthy (overrides tree type color)
            text_color = (0, 0, 0)  # Black text
        elif damage == 'LD':
            rect_color = (0, 255, 255)  # Darker Red for High Damage
            text_color = (0, 0, 0)  # Black text
        else:
            rect_color = (0, 0, 255)  # Darker Red for High Damage
            text_color = (0, 0, 0)  # Black text
    else:
        rect_color = (255, 0, 255)  # Red for other tree types
        text_color = (0, 0, 0)  # Black text

    # Draw bounding box on the image with color based on tree type and damage
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), rect_color, 2)
    
    # Get the text to display
    if tree_type == "Other":
        text = tree_type
    else:
        text = f"{tree_type} - {damage}"
    
    # Get the size of the text
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    
    # Draw a filled rectangle as background for text
    cv2.rectangle(image, (xmin, ymin - text_height - 5), (xmin + text_width, ymin), rect_color, -1)

    # Display tree type and damage information with the same color
    cv2.putText(image, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)

# Save the annotated image
annotated_image_path = "Test/annotated_photo1.jpg"  # Replace with your desired path
cv2.imwrite(annotated_image_path, image)
