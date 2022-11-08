from os import getcwd, listdir, makedirs
from os.path import exists, isfile, join

from neural_neighbor import neural_neighbor_style_transfer


def style_transfer_series(
    content_images_folder: str,
    style_image_path: str,
    output_folder: str,
    high_res=False,
):
    """Perform neural neighbour style transfer on all images in a folder.

    Args:
        content_images_folder (str): The folder of the source content images.
        style_image_path (str): The file path to the style image.
        output_folder (str): The output folder to create the style transferred images
            in. The style transferred images will have the same filename as their
            content source file in the output folder.
        high_res (bool, optional): If the output image should be high-res,
            being 1024px^2. By default creates 512px size images. Defaults to False.
    """
    folder_files = [
        file
        for file in listdir(content_images_folder)
        if isfile(join(content_images_folder, file))
    ]

    if not exists(output_folder):
        makedirs(output_folder)
        print(f"Creates directory {output_folder}")

    for file in folder_files:
        print(f"Executing style transfer on {file}")
        neural_neighbor_style_transfer(
            join(content_images_folder, file),
            style_image_path,
            join(output_folder, file),
            high_res=high_res,
        )
        print(f"Finished style transfer on {file}\n\n")


if __name__ == "__main__":
    print("cwd:", getcwd())
    style_transfer_series("./images/content", "./images/style/S1.jpg", "./images/new/")
