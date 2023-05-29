from typing import Tuple
import imageio
import numpy as np
import cv2


def load_gif(filename: str, target_size: Tuple[int]):
    arrs = imageio.mimread(filename)
    arrs = [np.transpose(arr[:, :, :3], (1, 0, 2)) for arr in arrs]
    h, w, _ = arrs[0].shape
    th, tw = target_size

    arrs = [cv2.resize(arr, (tw, th)) for arr in arrs]
    return arrs
