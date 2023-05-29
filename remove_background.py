from pathlib import Path
import cv2
import tqdm
import numpy as np

mask_images_folder = Path("split2")
target_images_folder = Path(
    r"C:\Users\espen\PycharmProjects\living_paintings\living_painting\raw_style_transfers"
)
output_folder = Path("preprocessed_images")
output_folder.mkdir(exist_ok=True)

sub_folders = list(target_images_folder.glob("*"))
mask_images_paths = mask_images_folder.glob("*")

threshold_lower = np.array([240, 240, 240])
threshold_higher = np.array([255, 255, 255])


mask_image_stems_to_file = {path.stem: path for path in mask_images_paths}

keys = list(mask_image_stems_to_file.keys())

for sub_folder in sub_folders:
    print(f"converting {str(sub_folder)}")
    target_images_paths = list(sub_folder.glob("*"))

    (output_folder / sub_folder.stem).mkdir(exist_ok=True)

    for target_path in tqdm.tqdm(target_images_paths):
        target_name = target_path.stem
        if target_name in keys:
            mask_path = mask_image_stems_to_file[target_name]
        else:
            print(target_name, keys)
            print(f"Couldn't find mask corresponding to {target_name}. Aborting")
            break
        target_image = cv2.imread(str(target_path))
        mask = cv2.imread(str(mask_path))
        backround = cv2.threshold(
            cv2.inRange(mask, threshold_lower, threshold_higher),
            127,
            255,
            cv2.THRESH_BINARY,
        )[1]
        (num_labels, labels_im) = cv2.connectedComponents(backround, connectivity=8)
        labels, area = np.unique(labels_im, return_counts=True)
        largest = np.argsort(area)[-1]
        mask = np.equal(labels_im, labels[largest])
        # print(contours)
        target_image = cv2.cvtColor(target_image, cv2.COLOR_RGB2RGBA)
        # target_image = cv2.drawContours(target_image, contours, -1, 255, 3)
        target_image[mask, 3] = 0
        cv2.imwrite(
            str(output_folder / sub_folder.stem / target_name) + ".png", target_image
        )
