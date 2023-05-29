from typing import Tuple
import numpy as np
from pathlib import Path
import pandas as pd
import cv2


def load_image_data(folder=Path("./preprocessed_data")):
    data = pd.read_csv(folder / "data.csv")
    return data


def get_closest_image(df: pd.DataFrame, angle_x: float, angle_y: float):
    closest = np.argmin(
        np.abs(df[["angle_x"]].values - angle_x)
        + np.abs((df[["angle_y"]].values - angle_y))
    )
    return df[["image_path"]].values[closest][0]


def load_image(path, target_height, folder=Path("./preprocessed_data/images2")):
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)

    image = image.swapaxes(0, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    width, height = image.shape[:2]
    scale_factor = target_height / height
    image = cv2.resize(image, (target_height, int(width * scale_factor)))
    return image


def get_new_frame(
    df: pd.DataFrame,
    angle_x: float,
    files,
    style_index,
    next_style_index,
    progress,
    resolution: Tuple[int],
) -> Tuple[np.ndarray, Tuple[int], bool]:
    """
    Gets the next frame of the application.
    This function is the controller that connects
    the different submodules together
    """
    needs_update = True
    block_size = 50
    width, height = resolution
    print(files.shape[1] * angle_x)
    index = np.min((np.floor(files.shape[1] * angle_x).astype(int), files.shape[1] - 1))
    image_path = files[style_index][index]
    image_path_2 = files[next_style_index][index]
    image = load_image(image_path, height)
    image2 = load_image(image_path_2, height)
    print(style_index, next_style_index)
    image = np.floor((image * (1 - progress) + image2 * (progress))).astype(int)
    image_width = image.shape[0]
    offset = (int((width - image_width) / 2), 0)
    center = np.array(
        (
            block_size / 2 + angle_x * (width - block_size),
            block_size / 2,
        ),
    ).astype(int)

    img = np.zeros((width, height), dtype=np.int)

    img[
        center[0] - block_size // 2 : center[0] + block_size // 2,
        center[1] - block_size // 2 : center[1] + block_size // 2,
    ] = 255

    return image, offset, needs_update
