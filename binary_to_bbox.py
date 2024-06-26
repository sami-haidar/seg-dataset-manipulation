# https://www.kaggle.com/code/farahalarbeed/convert-binary-masks-to-yolo-format
import numpy as np
import os
import cv2
import shutil

class_label = 1

mask_folder = './bbox_data/original/labels/DCTRinternals2/'
image_folder = './bbox_data/original/images/DCTRinternals2/'
# Create output directory if it doesn't exist
output_path = "./outputs"
output_label_path = output_path + "/labels"
output_image_path = output_path + "/images"
os.makedirs(output_path, exist_ok=True)
os.makedirs(output_path + '/images', exist_ok=True)
os.makedirs(output_path + '/labels', exist_ok=True)

image_names = os.listdir(image_folder)
image_paths = [os.path.join(image_folder, x) for x in image_names]
mask_paths = [os.path.join(mask_folder, x) for x in os.listdir(mask_folder)]

if class_label == 0:
    condition = 'no'
elif class_label == 1:
    condition = 'with'
else:
    raise RuntimeError("Script written for 2 classes: with and without blinds.")


def convert_coordinates_to_yolo(image_width, image_height, x, y, width, height):
    x_center = (x + width / 2) / image_width
    y_center = (y + height / 2) / image_height
    normalized_width = width / image_width
    normalized_height = height / image_height

    return x_center, y_center, normalized_width, normalized_height


def process_mask(mask, threshold = 128):
    _, binary_mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = np.zeros_like(mask)
    
    bounding_boxes = []
    i = 0
    for contour in contours:
        contour_image = np.zeros_like(mask)
        cv2.drawContours(contour_image, [contour], 0, 255, thickness=2)
        i += 1
        x, y, width, height = cv2.boundingRect(contour)
        x_center, y_center, normalized_width, normalized_height = convert_coordinates_to_yolo(mask.shape[1], mask.shape[0], x, y, width, height)
        bounding_boxes.append([class_label, x_center, y_center, normalized_width, normalized_height])

    return bounding_boxes


def write_yolo_annotations(output_path, annotation_name, bboxes, mask_height, mask_width, mask_class):
    annotation_file_path = os.path.join(output_label_path, annotation_name)

    too_few_points = False
    are_there_bboxes = False

    with open(annotation_file_path, "a+") as file:
        for bbox in bboxes:
            line = ''
            for item in bbox:
                line += f'{item} '
            line += '\n'

            file.write(line)
            are_there_bboxes = True
    

    if not are_there_bboxes:
        # shutil.rmtree(os.path.join(mask_folder, annotation_name.replace('.txt', '')))
        # os.remove(os.path.join(image_folder, annotation_name.replace('.txt', '.jpg')))
        print(f"{annotation_name}: No bboxes to save. Deleted from dataset, {too_few_points}")
    
    print(f"{annotation_name} done")


total_images = 0
for i, mask_path in enumerate(mask_paths):

    # Deal with some masks being windows, doors, etc... AND FILTER THROUGH THOSE WITH OR WITHOUT BLINDS
    masks_in_image = [os.path.join(mask_path, x) for x in os.listdir(mask_path) if condition in x]
    total_images += 1 if len(masks_in_image) else 0

    for mask_in_image in masks_in_image:
        mask = cv2.imread(mask_in_image, cv2.IMREAD_GRAYSCALE)

        if mask is None:
            continue

        mask_height = mask.shape[0]
        mask_width = mask.shape[1]
        annotation_name = mask_in_image.replace(mask_folder, '').split('/')[0] + '.txt'
        mask_name = mask_in_image.replace(mask_folder, '').split('/')[1]

        print(mask_in_image)
        image_name = mask_in_image.replace(mask_folder, '').split('/')[0] + '.JPG'
        image_path = os.path.join(image_folder, image_name)
        shutil.copy(image_path, os.path.join(output_image_path, image_name))

        bboxes = process_mask(mask)
        if not bboxes:            
            print(mask_path)
            print(image_folder, mask_path.replace(mask_folder, '') + '.jpg')
            continue
        write_yolo_annotations(output_path, annotation_name, bboxes, mask_height, mask_width, class_label)

    if total_images >= 200: 
        print("Max images reached. Stopping")
        break
