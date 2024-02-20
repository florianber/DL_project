import cv2
import xml.etree.ElementTree as ET

# Load XML annotation

FILE = "B01_0021"
xml_file = f"Data/Bebehojd_20190527/Annotations/{FILE}.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Load image
image_path = f"Data/Bebehojd_20190527/Images/{FILE}.JPG"
image = cv2.imread(image_path)

# Iterate through objects in the XML and draw bounding boxes with different colors
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
            text_color = (0, 255, 0)
        elif damage == 'LD':
            rect_color = (0, 255, 255)  # Darker Red for High Damage
            text_color = (0, 255, 255)
        else:
            rect_color = (0, 0, 255)  # Darker Red for High Damage
            text_color = (0, 0, 255)
    else:
        rect_color = (255, 0, 255)  # Red for other tree types
        text_color = (255, 0, 255)



    # Draw bounding box on the image with color based on tree type and damage
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), rect_color, 2)
    
    # Display tree type and damage information with the same color
    cv2.putText(image, f"{tree_type} - {damage}", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)



# Save the annotated image
annotated_image_path = "annotated_photo.jpg"  # Replace with your desired path
cv2.imwrite(annotated_image_path, image)

