import os
import cv2
from uuid import uuid4
import json

dataset_names = ['DCTR', 'Blinklab', 'uriel']
train_or_val = 'train'

output = f'window-pull_{train_or_val}.json'

dataset_json = {}
dataset_json["info"] = {
    "description": "Window Pull Repository - DCTR, Blinklab and dec2023 data",
    "version": "1.0",
    "year": 2024,
    "contributor": "Autoenhance.ai",
    "date_created": "22 Feb 2024"
}
dataset_json["licenses"] = [{
    "url": "tbd",
    "id": 1,
    "name": "tbd"
}]

dataset_json["images"] = []
dataset_json["annotations"] = []

dataset_json["categories"] = [{
    "supercategory": "window",
    "id": 1,
    "name": "window"
}]

image_id = 0
mask_id = 0

for dataset_name in dataset_names:
    input_path = f'{dataset_name}/images/{train_or_val}'
    labels_path = f'{dataset_name}/labels/{train_or_val}'

    inputs = os.listdir(input_path)
    labels = os.listdir(labels_path)

    print(f"Processing {input_path} with labels {labels_path}")

    for input in inputs:
        image_data = {}

        img = cv2.imread(os.path.join(input_path, input))
        height, width = img.shape[:2]

        image_data["file_name"] = input
        image_data["license"] = 1
        image_data["id"] = image_id
        image_data["height"] = height
        image_data["width"] = width

        label_filepath = os.path.join(labels_path, input.split('.')[0] + '.txt')
        try:
            with open(label_filepath) as label_file:
                for segment in label_file:
                    annotation = {}
                    category = segment[0]
                    points = segment[2:].split(' ')
                    coco_points = []
                    is_odd = True
                    for point in points:
                        if point == '\n':
                            continue
                        if is_odd:
                            coco_points.append(float(point) * width)
                        else:
                            coco_points.append(float(point) * height)
                        is_odd = not is_odd
                    
                    bbox_x0 = min(coco_points[::2])
                    bbox_x1 = max(coco_points[::2])
                    bbox_y0 = min(coco_points[1::2])
                    bbox_y1 = max(coco_points[1::2])
                    bbox_h = bbox_y1 - bbox_y0
                    bbox_w = bbox_x1 - bbox_x0

                    annotation["image_id"] = image_id
                    annotation["segmentation"] = [coco_points]
                    annotation["iscrowd"] = 0
                    annotation["category_id"] = category
                    annotation["id"] = mask_id
                    annotation["bbox"] = [
                        bbox_x0,
                        bbox_y0,
                        bbox_w,
                        bbox_h
                    ]

                    dataset_json["annotations"].append(annotation)
                    mask_id += 1
        except FileNotFoundError:
            # print(f"WARNING! Mask not found. {input}")
            pass

        image_id += 1
print(f"{image_id} images processed correctly")
print(f"{mask_id} segments added.")
    

with open(output, "w+") as output_file:
    json.dump(dataset_json, output_file)