import os

def lire_fichier_texte(chemin_fichier, dossier_labels):
    with open(dossier_labels + chemin_fichier, 'r') as file:
        lines = file.readlines()
        # On suppose ici que chaque ligne du fichier correspond à une annotation
        annotations = [line.strip().split() for line in lines]
    return annotations

# Calucule la proportion de chaque type d'arbre d'une photo à partir des labels 
def calculer_proportion_arbres(annotations, int_to_labels):
    proportions = {label: 0 for label in int_to_labels.values()}
    print(len(annotations))
    if len(annotations)  != 0:
        total_arbres = len(annotations)

        for annotation in annotations:
            # La première colonne représente le type d'arbre
            type_arbre = int(annotation[0])
            label = int_to_labels[type_arbre]
            proportions[label] += 1

        # Calculer les proportions
        proportions = {label: count / total_arbres for label, count in proportions.items()}
    return proportions

def obtenir_proportions_par_image(dossier_labels, int_to_labels):
    proportions_par_image = {}

    # Liste des noms de fichiers dans le dossier
    noms_fichiers = os.listdir(dossier_labels)

    for nom_fichier in noms_fichiers:
        print(nom_fichier)
        # Charger les données du fichier texte
        annotations = lire_fichier_texte(nom_fichier, dossier_labels)
        print(len(annotations))

        # Calculer les proportions pour ce fichier
        proportions_fichier = calculer_proportion_arbres(annotations, int_to_labels)

        # Ajouter les proportions de ce fichier à la liste
        proportions_par_image[nom_fichier] = proportions_fichier

    return proportions_par_image

# Afficher les proportions pour chaque image
def stats(proportions_par_image):
    image_a_augmenter = []
    
    for nom_image, proportions in proportions_par_image.items():
        print(f"{nom_image}:")
        for label, proportion in proportions.items():
            print(f"   {label}: {proportion * 100:.2f}%")
        proportion_H = proportions.get("Larch-H", 0)
        proportion_HD = proportions.get("Larch-HD", 0)

        # Ajouter le nom de la photo à la liste si la proportion de H ou HD est supérieure à 30%
        if proportion_H > 0.3 or proportion_HD > 0.3:
            image_a_augmenter.append(nom_image)
    return image_a_augmenter


dossier_labels_train = 'Data/train/labels/'
dossier_labels_valid = 'Data/valid/labels/'
int_to_labels = {0: "Other", 1: "Larch-H", 2: "Larch-LD", 3: "Larch-HD"}

proportions_par_image_train = obtenir_proportions_par_image(dossier_labels_train, int_to_labels)
proportions_par_image_valid = obtenir_proportions_par_image(dossier_labels_valid, int_to_labels)

augmented_images_train = stats(proportions_par_image_train)
augmented_images_valid = stats(proportions_par_image_valid)

import os
from imgaug import augmenters as iaa
from PIL import Image
import numpy as np
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

def lire_fichier_texte(chemin_fichier):
    with open(chemin_fichier, 'r') as file:
        lines = file.readlines()
        # On suppose ici que chaque ligne du fichier correspond à une annotation
        annotations = [line.strip().split() for line in lines]
    return annotations

def ecrire_fichier_texte(chemin_fichier, annotations):
    with open(chemin_fichier, 'w') as file:
        for annotation in annotations:
            line = ' '.join(map(str, annotation)) + '\n'
            file.write(line)

def appliquer_data_augmentation(images_dir, labels_dir, image_names, output_dir):
    # Créer un séquenceur d'augmentation d'images
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),   # Flip horizontal
        iaa.Flipud(0.5),   # Flip vertical
        iaa.Affine(rotate=(-45, 45)),   # Rotation
        iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 1.0))),   # Flou gaussien
        # Ajoutez d'autres transformations selon vos besoins
    ])
    # Créer les dossiers de sortie s'ils n'existent pas
    output_images_dir = os.path.join(output_dir, 'images')
    output_labels_dir = os.path.join(output_dir, 'labels')
    
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)    

    for image_name in image_names:
        print(image_name)
        # Charger l'image
        image_path = os.path.join(images_dir, image_name.replace('.txt', '.JPG'))
        image = Image.open(image_path)

        # Charger les annotations
        label_path = os.path.join(labels_dir, image_name)
        annotations = lire_fichier_texte(label_path)


        # Convertir les annotations en objets imgaug
        bbs = []
        for annotation in annotations:
            x, y, w, h = map(float, annotation[1:])
            bbs.append(BoundingBox(x1=x, y1=y, x2=x + w, y2=y + h))
        
        # Créer un objet imgaug pour les annotations
        bbs = BoundingBoxesOnImage(bbs, shape=image.size)

        # Appliquer la data augmentation
        augmented_image, augmented_bbs = seq(image=np.array(image), bounding_boxes=bbs)
        augmented_image = Image.fromarray(augmented_image)

        # Sauvegarder l'image augmentée
        output_image_path = os.path.join(output_images_dir, image_name.replace('.txt', '.JPG'))
        augmented_image.save(output_image_path)
        
        # Mettre à jour et sauvegarder les annotations
        updated_annotations = [[str(idx)] + [bb.x1, bb.y1, bb.x2, bb.y2] for idx, bb in enumerate(augmented_bbs.bounding_boxes)]
        output_label_path = os.path.join(output_labels_dir, image_name.replace('.jpg', '.txt'))
        ecrire_fichier_texte(output_label_path.replace('.jpg', '.txt'), updated_annotations)

# Exemple d'utilisation
dossier_data = 'Data'
dossier_train = os.path.join(dossier_data, 'train')
dossier_valid = os.path.join(dossier_data, 'valid')

dossier_images_train = os.path.join(dossier_train, 'images')
dossier_labels_train = os.path.join(dossier_train, 'labels')

dossier_images_valid = os.path.join(dossier_valid, 'images')
dossier_labels_valid = os.path.join(dossier_valid, 'labels')

# Dossier de sortie pour les images augmentées
output_dir = 'Data/DataAugmentation'

# Appliquer la data augmentation aux images d'entraînement
appliquer_data_augmentation(dossier_images_train, dossier_labels_train, augmented_images_train, output_dir)
