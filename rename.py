import os

# Filter through Uriel's dataset by taking only final images and masks.

input_path = 'data/images/'

inputs = sorted(os.listdir(input_path))

found_images = []
for input in inputs:
    name_in = input.split('final')[0] + 'window.jpg'
    os.rename(os.path.join(input_path, input), os.path.join(input_path, name_in))