import os
from pathlib import Path
import cv2
def resize(folder=Path("E:/images"), output_folder=Path("E:/images_resized")):
    files = list(folder.glob("**/*.*"))
    output_folder.mkdir(exist_ok=True)

    for file in files:
        image = cv2.imread(str(file))
        x,y,_ = image.shape
        image = cv2.resize(image,(y//2, x//2))
        filename = file.name
        cv2.imwrite(str(output_folder/filename),image)

resize()