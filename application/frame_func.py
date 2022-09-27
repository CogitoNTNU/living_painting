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
    delta_time /= 100
    block_size = 50
    time /= 1000
    width, height = resolution
    print(delta_time)
    center = (
        np.array((width // 2, height // 2))
        + 200 * np.array((np.cos(time), np.sin(time)))
    ).astype(int)
    print(center)
    img = np.zeros((width, height), dtype=np.int)
    # img = np.arange(resolution[0]).repeat(resolution[1], axis=0)

    img[
        center[0] - block_size : center[0] + block_size,
        center[1] - block_size : center[1] + block_size,
    ] = 255

    print(img.shape)
    return img, needs_update
