from typing import Tuple
import numpy as np


def get_new_frame(
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

    return img, needs_update
