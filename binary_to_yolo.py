# Adapted from https://www.kaggle.com/code/farahalarbeed/convert-binary-masks-to-yolo-format

import numpy as np

import os
from PIL import Image
import cv2
import os
import shutil

mask_folder = 'data/DCTRlabels/'
image_folder = 'data/DCTR/'

image_names = os.listdir(image_folder)
image_paths = [os.path.join(image_folder, x) for x in image_names]
# mask_paths = [os.path.join(mask_folder, x, '0_window no blinds.png') for x in os.listdir(mask_folder)]
mask_paths = [os.path.join(mask_folder, x) for x in os.listdir(mask_folder)]


def process_mask(mask, threshold = 128):
    # Image processing
    _, binary_mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = np.zeros_like(mask)
    
    i = 0
    for contour in contours:
        contour_image = np.zeros_like(mask)
        cv2.drawContours(contour_image, [contour], 0, 255, thickness=2)
        # contour_tosave = Image.fromarray(contour_image)
        # if i % 50 == 0:
        #     contour_tosave.save(f'cont{i}.png')
        i += 1

    return contours


def write_yolo_annotations(output_path, annotation_name, contours, mask_height, mask_width, mask_class):
    annotation_file_path = os.path.join(output_path, annotation_name)

    too_few_points = False
    are_there_contours = False

    # FILE OPENED AS APPENDING!!! DELETE PRE-EXISTING CONTOUR FILES BEFORE RE-RUNNING
    with open(annotation_file_path, "a+") as file:
        for contour in contours:
            # print(contour.shape)
            squeezed_contour = np.squeeze(contour)
            # print(squeezed_contour.shape)

            if len(squeezed_contour.shape) < 2:
                # print(squeezed_contour.shape, squeezed_contour)
                # print(annotation_name)
                continue

            num_points, _ = squeezed_contour.shape
            if num_points < 3:
                print("ONLY 2 POINTS IN CONTOUR!", squeezed_contour.shape, squeezed_contour, annotation_name)
                too_few_points = True
                continue

            line = f'{mask_class} '
            for point in squeezed_contour:
                line += f"{point[0] / mask_width} {point[1] / mask_height} "
            
            line += '\n'
            file.write(line)
            are_there_contours = True
    

    if not are_there_contours:
        # shutil.rmtree(os.path.join(mask_folder, annotation_name.replace('.txt', '')))
        # os.remove(os.path.join(image_folder, annotation_name.replace('.txt', '.jpg')))
        print(f"{annotation_name}: No contours to save. Deleted from dataset, {too_few_points}")
    
    # print(f"{annotation_name} done")


# Create output directory if it doesn't exist
output_path = "./outputs"
os.makedirs(output_path, exist_ok=True)

for mask_path in mask_paths:

    # Deal with some masks being windows, doors, etc...
    masks_in_image = [os.path.join(mask_path, x) for x in os.listdir(mask_path)]

    for mask_in_image in masks_in_image:
        mask = cv2.imread(mask_in_image, cv2.IMREAD_GRAYSCALE)

        if mask is None:
            # os.remove(mask_path)
            # os.remove(os.path.join(image_folder, mask_path.replace(mask_folder, '') + '.jpg'))
            continue

        mask_height = mask.shape[0]
        mask_width = mask.shape[1]
        
        # annotation_name = mask_path.replace(mask_folder, '').split('/')[0] + '.txt'
        # mask_name = mask_path.replace(mask_folder, '').split('/')[1]        
        annotation_name = mask_in_image.replace(mask_folder, '').split('/')[0] + '.txt'
        mask_name = mask_in_image.replace(mask_folder, '').split('/')[1]

        mask_class = None
        # if 'window no blinds' in mask_name:
        #     mask_class = 0
        # elif 'window with blinds' in mask_name:
        #     mask_class = 1
        # elif 'door no blinds' in mask_name:
        #     mask_class = 2
        # elif 'door with blinds' in mask_name:
        #     mask_class = 3
        # else:
        #     raise RuntimeError

        if 'window no blinds' in mask_name:
            mask_class = 0
        elif 'window with blinds' in mask_name:
            mask_class = 0
        elif 'door no blinds' in mask_name:
            mask_class = 0
        elif 'door with blinds' in mask_name:
            mask_class = 0
        else:
            raise RuntimeError

        # annotation_name = os.path.basename(mask_path).replace(".png", ".txt")

        contours = process_mask(mask)
        if not contours:            
            print(mask_path)
            print(image_folder, mask_path.replace(mask_folder, '') + '.jpg')
            continue
            # raise RuntimeError
        write_yolo_annotations(output_path, annotation_name, contours, mask_height, mask_width, mask_class)