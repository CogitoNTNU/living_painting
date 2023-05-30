from pathlib import Path
import cv2
import pandas as pd
import numpy as np
import os
import time


def preprocess():
    capture = cv2.VideoCapture("vid.mp4")

    image_store = Path("preprocessed_data/images5")
    spreadsheet_store = Path("preprocessed_data")

    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frameNr = 0

    df = pd.DataFrame(columns=["image_path", "angle_x"])

    spreadsheet_store.mkdir(exist_ok=True)

    angles = []
    angles_y = []
    filenames = []
    image_store.mkdir(exist_ok=True)
    for i in range(length):
        success, frame = capture.read()
        filename = image_store / f"{i}.jpg"
        angle = i / (length - 1)
        angles.append(angle)
        angles_y.append(0.45)
        filenames.append(filename)
        cv2.imwrite(str(filename), frame)
    df = pd.DataFrame({"image_path": filenames, "angle_x": angles, "angle_y": angles_y})
    df.to_csv(spreadsheet_store / "data.csv", index=False)


def preprocess_folder():
    parent_dir = Path(
        r"C:\Users\espen\PycharmProjects\living_paintings\living_painting\background_removed"
    )
    files = list(parent_dir.glob("**/*"))

    spreadsheet_store = Path("preprocessed_data")

    length = len(files)

    print(f"processing {length} images")
    df = pd.DataFrame(columns=["image_path", "angle_x"])

    spreadsheet_store.mkdir(exist_ok=True)

    angles_x = []
    angles_y = []

    max_x = len(files)
    max_y = 1
    filenames = []
    for x in range(max_x):
        for y in range(max_y):
            filename = str(files[x])
            angle_x = x / max_x
            angles_x.append(angle_x)
            angle_y = 0.45 + (y / max_y) * 0.1
            angles_y.append(angle_y)
            filenames.append(filename)
    df = pd.DataFrame(
        {"image_path": filenames, "angle_x": angles_x, "angle_y": angles_y}
    )
    df.to_csv(spreadsheet_store / "data.csv", index=False)


def preprocess_folders():
    parent_dir = Path(
        r"C:\Users\espen\PycharmProjects\living_paintings\living_painting\preprocessed_images"
    )
    sub_folders = list(parent_dir.glob("*"))

    spreadsheet_store = Path("preprocessed_data")

    files = []
    stems = []
    for i, sub_folder in enumerate(sub_folders):
        files.append(
            list(str(parent_dir / sub_file) for sub_file in sub_folder.glob("*"))
        )
        stems.append([int(file.stem) for file in sub_folder.glob("*")])
    stems = np.array(stems)
    files = np.array(files)
    min_val = np.min(stems)
    max_val = np.max(stems)
    angles = (stems - min_val) / max_val
    print(files.shape)
    print(files)
    files = np.save("paths.npy", files)
