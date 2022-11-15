from pathlib import Path
import cv2
import pandas as pd
import numpy as np
import os


def preprocess():
    capture = cv2.VideoCapture("data/trimmed.mp4")

    image_store = Path("preprocessed_data/images2")
    spreadsheet_store = Path("preprocessed_data")

    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frameNr = 0

    df = pd.DataFrame(columns=["image_path", "angle_x"])

    spreadsheet_store.mkdir(exist_ok=True)

    angles = []
    filenames = []
    image_store.mkdir(exist_ok=True)
    for i in range(length):
        success, frame = capture.read()
        filename = image_store / f"{i}.jpg"
        angle = i / (length - 1)
        angles.append(angle)
        filenames.append(filename)
        cv2.imwrite(str(filename), frame)
    df = pd.DataFrame({"image_path": filenames, "angle_x": angles})
    df.to_csv(spreadsheet_store / "data.csv", index=False)


def preprocess_folder():
    start_index = 200
    parent_dir = Path("C:\\Users\\espen\\Documents\\new")
    files = list(parent_dir.glob("**/*"))

    image_store = Path("preprocessed_data/images3")
    spreadsheet_store = Path("preprocessed_data")

    length = len(files)

    print(f"processing {length} images")
    df = pd.DataFrame(columns=["image_path", "angle_x"])

    spreadsheet_store.mkdir(exist_ok=True)

    angles_x = []
    angles_y = []

    max_x = 201
    max_y = 1
    filenames = []
    image_store.mkdir(exist_ok=True)
    for x in range(max_x):
        for y in range(max_y):
            filename = parent_dir / f"{y}_{x}.png"
            angle_x = x / max_x
            angles_x.append(angle_x)
            angle_y = 0.45 + (y / max_y) * 0.1
            angles_y.append(angle_y)
            filenames.append(filename)
    df = pd.DataFrame(
        {"image_path": filenames, "angle_x": angles_x, "angle_y": angles_y}
    )
    df.to_csv(spreadsheet_store / "data.csv", index=False)
