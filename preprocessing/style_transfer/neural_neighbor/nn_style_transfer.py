import random
import time
from typing import Literal, Union

import numpy as np
import torch
from imageio import imwrite

from .pretrained.vgg import Vgg16Pretrained
from .utils import misc as misc
from .utils.misc import load_path_for_pytorch
from .utils.stylize import produce_stylization

# Fix Random Seed

# Define command line parser and get command line arguments
# parser = argparse.ArgumentParser()
# parser.add_argument("--content_path", type=str, default=None, required=True)
# parser.add_argument("--style_path", type=str, default=None, required=True)
# parser.add_argument("--output_path", type=str, default=None, required=True)
# parser.add_argument("--high_res", action="store_true")
# parser.add_argument("--cpu", action="store_true")
# parser.add_argument("--no_flip", action="store_true")
# parser.add_argument("--content_loss", action="store_true")
# parser.add_argument("--dont_colorize", action="store_true")
# parser.add_argument("--alpha", type=float, default=0.75)
# args = parser.parse_args()


def neural_neighbor_style_transfer(
    content_path: str,
    style_path: str,
    output_path: str,
    high_res=False,
    cpu=False,
    no_flip=False,
    content_loss=False,
    dont_colorize=False,
    alpha=False,
    size: Union[Literal[256], Literal[512], Literal[1024]] = 512,
):
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)
    max_scls = 3
    sz = size
    if high_res:
        max_scls = 5
        sz = 1024
    flip_aug = not no_flip
    misc.USE_GPU = not cpu
    content_weight = 1.0 - alpha

    # Error checking for arguments
    # error checking for paths deferred to imageio
    assert (0.0 <= content_weight) and (
        content_weight <= 1.0
    ), "alpha must be between 0 and 1"
    assert torch.cuda.is_available() or (
        not misc.USE_GPU
    ), "attempted to use gpu when unavailable"

    # Define feature extractor
    cnn = misc.to_device(Vgg16Pretrained())

    def phi(x, y, z):
        return cnn.forward(x, inds=y, concat=z)

    # Load images
    content_im_orig = misc.to_device(
        load_path_for_pytorch(content_path, target_size=sz)
    ).unsqueeze(0)
    style_im_orig = misc.to_device(
        load_path_for_pytorch(style_path, target_size=sz)
    ).unsqueeze(0)

    # Run Style Transfer
    torch.cuda.synchronize()
    start_time = time.time()
    output = produce_stylization(
        content_im_orig,
        style_im_orig,
        phi,
        max_iter=200,
        lr=2e-3,
        content_weight=content_weight,
        max_scls=max_scls,
        flip_aug=flip_aug,
        content_loss=content_loss,
        dont_colorize=dont_colorize,
    )
    torch.cuda.synchronize()
    print("Done! total time: {}".format(time.time() - start_time))

    # Convert from pyTorch to numpy, clip to valid range
    new_im_out = np.clip(output[0].permute(1, 2, 0).detach().cpu().numpy(), 0.0, 1.0)

    # Save stylized output
    save_im = (new_im_out * 255).astype(np.uint8)
    imwrite(output_path, save_im)

    # Free gpu memory in case something else needs it later
    if misc.USE_GPU:
        torch.cuda.empty_cache()
