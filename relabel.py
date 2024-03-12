# Reorganise data with folder structure required by model
# Note that these won't be the real masks, I'm just assigning
# blindly window no blind to all of them

import os

base_path = 'data/masks'
out_path = 'data/final_masks'

mask_inputs = [ name for name in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, name)) ]

for mask_name in mask_inputs:
    out_folder_name = mask_name.split('.')[0]
    out_mask_name = '0_window no blinds.png'

    if os.path.isdir(os.path.join(out_path, out_folder_name)):
        continue

    os.mkdir(os.path.join(out_path, out_folder_name))
    os.replace(
        os.path.join(base_path, mask_name), 
        os.path.join(out_path, out_folder_name, out_mask_name)
    )
