import os
import xml.etree.ElementTree as ET

def count_trees_and_damage(xml_file):
    tree_damage_counts = {}

    tree = ET.parse(xml_file).getroot()

    for obj in tree.findall('.//object'):
        tree_type = obj.find('tree').text
        damage_type = obj.find('damage').text

        key = (tree_type, damage_type)
        tree_damage_counts[key] = tree_damage_counts.get(key, 0) + 1

    return tree_damage_counts

def process_directory(directory_path):
    tree_damage_counts = {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".xml"):
            xml_file = os.path.join(directory_path, filename)
            counts = count_trees_and_damage(xml_file)

            for key, count in counts.items():
                tree_damage_counts[key] = tree_damage_counts.get(key, 0) + count

    return tree_damage_counts

if __name__ == "__main__":
    directory_path = "path/to/your/xml/files"
    result = process_directory(directory_path)

    for key, count in result.items():
        print(f"Tree: {key[0]}, Damage: {key[1]}, Count: {count}")