import cv2
import os
import numpy as np


labels_path = "data/labels"
saving_path = "data/masks"
masks_paths = [ name for name in os.listdir(labels_path) if os.path.isfile(os.path.join(labels_path, name)) ]

for mask_path in masks_paths:
    img = cv2.imread(os.path.join(labels_path, mask_path), cv2.IMREAD_UNCHANGED)

    mask = (img[:, :, 3] > 0).astype(int) * 65535
    img[:, :, 0] = mask
    img[:, :, 1] = mask
    img[:, :, 2] = mask
    img = img[:, :, :3]

    cv2.imwrite(os.path.join(saving_path, mask_path), img)