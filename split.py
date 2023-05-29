import cv2

vidcap = cv2.VideoCapture(r"vid2.mp4")
output_folder_1 = "split"
output_folder_2 = "split2"
success, image = vidcap.read()
count = 0

while success:
    if count % 60 == 0:
        cv2.imwrite(
            f"{output_folder_1}/{str(count).rjust(5, '0')}.jpg",
            image[: 512 * 2, 512 : 512 * 3],
        )  # save frame as JPEG file
        print(f"saved number {count}")
    cv2.imwrite(
        f"{output_folder_2}/{str(count).rjust(5, '0')}.jpg",
        cv2.resize(image[: 512 * 2, 512 : 512 * 3], (512, 512)),
    )  # save frame as JPEG file
    success, image = vidcap.read()
    count += 1
