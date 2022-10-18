from typing import Tuple
import numpy as np
from pathlib import Path
import pandas as pd
import cv2


def load_image_data(folder=Path("./preprocessed_data")):
    data = pd.read_csv(folder / "data.csv")
    return data


def get_closest_image(df: pd.DataFrame, angle_x: float, angle_y: float):
    closest = np.argmin(np.abs(df[["angle_x"]].values - angle_x))
    return df[["image_path"]].values[closest][0]


def load_image(path, target_height, folder=Path("./preprocessed_data/images2")):
    image = cv2.imread(str(path))

    image = image.swapaxes(0, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    width, height = image.shape[:2]
    scale_factor = target_height / height
    image = cv2.resize(image, (target_height, int(width * scale_factor)))
    return image


def get_new_frame(
    df: pd.DataFrame,
    angle_x: float,
    angle_y: float,
    time: float,
    delta_time: float,
    resolution: Tuple[int],
) -> Tuple[np.ndarray, bool]:
    """
    Gets the next frame of the application.
    This function is the controller that connects
    the different submodules together
    """
    needs_update = True
    block_size = 50
    width, height = resolution
    image_path = get_closest_image(df, angle_x, angle_y)
    image = load_image(image_path, height)
    image_width = image.shape[0]
    offset = (int((width - image_width) / 2), 0)
    center = np.array(
        (
            block_size / 2 + angle_x * (width - block_size),
            block_size / 2 + angle_y * (height - block_size),
        ),
    ).astype(int)

    img = np.zeros((width, height), dtype=np.int)

    img[
        center[0] - block_size // 2 : center[0] + block_size // 2,
        center[1] - block_size // 2 : center[1] + block_size // 2,
    ] = 255

    return image, offset, needs_update
