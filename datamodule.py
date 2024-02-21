from imports import *  # Assuming necessary imports are included in 'imports' module

def is_not_annotated(category_path):
    """
    Check if the category path is not annotated (ends with '7').
    """
    return category_path[-1] != "7"

def create_directory(directory_path):
    """
    Remove the entire directory and recreate it.
    """
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)
    else :
        os.makedirs(directory_path)

def get_files_and_path(source, category, directory_to_create):
    """
    Get files and paths for a given category.

    Parameters:
    - source: Source directory path
    - category: Category name
    - directory_to_create: List of directories to create

    Returns:
    - annotation_files: List of annotation files
    - image_files: List of image files
    - annotation_path: Path to annotations directory
    - image_path: Path to images directory
    """
    category_path = os.path.join(source, category)
    if is_not_annotated(category_path) or category_path in directory_to_create:
        return 0, 0, 0, 0
    else:
        annotations = os.listdir(category_path)[0]
        images = os.listdir(category_path)[1]
        annotation_path = os.path.join(source, category, annotations)
        image_path = os.path.join(source, category, images)
        annotation_files = sorted(os.listdir(annotation_path))
        image_files = sorted(os.listdir(image_path))
        return annotation_files, image_files, annotation_path, image_path

def gather_image_annotation(annotation_files, image_files):
    """
    Gather pairs of annotation and image files.

    Parameters:
    - annotation_files: List of annotation files
    - image_files: List of image files

    Returns:
    - gathered_files: List of pairs (annotation, image)
    """
    gathered_files = []
    for annotation in annotation_files:
        for image in image_files:
            if annotation.split(".")[0] in image:
                gathered_files.append((annotation, image))
                continue
    return gathered_files

def split_spot(gathered_list, split_ratio):
    """
    Split a list based on the specified ratio.

    Parameters:
    - gathered_list: List to split
    - split_ratio: Tuple of ratios (train, test)

    Returns:
    - train_split: Index for train split
    - test_split: Index for test split
    """
    train_split = int(split_ratio[0] * len(gathered_list))
    test_split = train_split + int(split_ratio[1] * len(gathered_list))
    return train_split, test_split

def create_src_path(anot_imag, annotations_path, images_path):
    """
    Create source paths for annotation and image.

    Parameters:
    - anot_imag: Tuple of annotation and image file names
    - annotations_path: Path to annotations directory
    - images_path: Path to images directory

    Returns:
    - src_path_annotation: Source path for annotation
    - src_path_image: Source path for image
    """
    annotation = anot_imag[0]
    image = anot_imag[1]
    src_path_annotation = os.path.join(annotations_path, annotation)
    src_path_image = os.path.join(images_path, image)
    return src_path_annotation, src_path_image
