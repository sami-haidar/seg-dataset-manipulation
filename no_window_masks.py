import os
import cv2
from pathlib import Path

# Filter through Uriel's dataset by taking only final images and masks.

input_path = 'data/DCTR/'
mask_path = 'outputs/'
saving_path = 'data/zero_masks/'
mask_file_name = '0_window no blinds.png'

csv_in_path = '/home/sami/workspace/window-pull-training/data_csv/DCTR_blink_dec2023data.csv'

inputs = sorted(os.listdir(input_path))
masks = sorted(os.listdir(mask_path))

dataset_images = {}
dataset_labels = {}

# found_images = []
# for mask in masks:
#     name_in = mask.split('window')[0] + 'final.jpg'
#     found_images.append(name_in)

    # row = '0,0,0,0,0,0,0,0,0,' 
    # row += name_in + ','
    # row += input_path.split('data/images/')[1] + name_in + ','
    # row += dataset + ','
    # row += mask_path.split('data/labels/')[1] + mask + ','
    # row += '1,0,0,0,1,0,9,' + name_in
    
    # print(row)


i = 0
# Some final images were still there even if they had no windows. Filter through
for final in inputs:
    # if final not in found_images:
    #     print(os.path.join(input_path, final))
    #     img = cv2.imread(os.path.join(input_path, final), cv2.IMREAD_UNCHANGED)
    #     print(img)
    #     img = img * 0

    #     mask_folder = final.split('final')[0] + 'window'

    #     os.mkdir(os.path.join(saving_path, mask_folder))
    #     cv2.imwrite(os.path.join(saving_path, mask_folder, mask_file_name), img)
    #     print(f"Found {final}!", os.path.join(input_path, final))
    # if final in found_images:
        # print(os.path.join(input_path, final))

        # to_remove = Path(os.path.join(input_path, final))
        # to_remove.unlink()
        # print(f"Deleted {final}!", os.path.join(input_path, final))
    if final.replace('.jpg', '') not in [x.replace('.txt', '') for x in masks]:
        print(os.path.join(input_path, final))

        to_remove = Path(os.path.join(input_path, final))
        to_remove.unlink()
        print(f"Deleted {final}!", os.path.join(input_path, final))
        i+=1

print(i, len(inputs), len(masks))