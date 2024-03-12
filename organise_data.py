import os

# Filter through Uriel's dataset by taking only final images and masks.

base_path = 'data/'

image_folders = [ name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name)) ]
print(image_folders)

dataset_images = {}
dataset_labels = {}

# Filter through the images that are labels and find their corresponding baselines.
# Error check for potential missing baselines, given a window label
for folder in image_folders:
    folder_path = os.path.join(base_path, folder)
    images = os.listdir(folder_path)
    keywords_to_keep = ['window', 'final']

    images_in_folder = []
    labels_in_folder = []
    for image in images:
        if 'window' in image:
            labels_in_folder.append(os.path.join(folder_path, image))
        else:
            continue

        baseline = image.split('window')[0] + "final.jpg"
        if baseline in images:
            images_in_folder.append(os.path.join(folder_path, baseline))
        else:
            print(images)
            raise RuntimeError(f"Found a label without baseline: {baseline} does not exist")
        
    if len(images_in_folder) != len(labels_in_folder):
        raise RuntimeError(f"Found a different number of inputs than labels: {len(images_in_folder)} images, {len(labels_in_folder)} labels")
    dataset_images[folder] = images_in_folder
    dataset_labels[folder] = labels_in_folder


# Move found labels and images
for folder in dataset_labels:
    for label in dataset_labels[folder]:
        file = os.path.basename(label)

        # Some labeled windows have misconstructed names, fixing here
        file = file.split("png")[0].strip() + ".png"

        destination_path = "data/labels"
        os.replace(label, os.path.join(destination_path, file))

for folder in dataset_images:
    for image in dataset_images[folder]:
        file = os.path.basename(image)
        destination_path = "data/images"
        os.replace(image, os.path.join(destination_path, file))

print(dataset_images.keys())
