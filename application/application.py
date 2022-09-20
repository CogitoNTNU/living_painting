import time
import cv2
import numpy as np

WINDOW_NAME = "Living painting"


class TimeHandler:
    def __init__(self, target_framerate: int = 24) -> None:
        self.target_framerate = target_framerate
        self.start_time = time.time()
        self.frame_time = self.start_time

    def get_wait_time(self) -> int:
        """In milliseconds"""
        end_time = time.time()
        diff_time = self.frame_time - end_time
        wait_time = int((1000 - diff_time * 1000) / self.target_framerate)
        return wait_time

    def reset(self):
        self.frame_time = time.time()

    def get_time_from_start(self) -> float:
        """In seconds"""
        return time.time() - self.start_time


def setup(window_name):
    """
    TODO: Fix aspect ratio
    """
    print(f"{cv2.WND_PROP_FULLSCREEN:b}")
    cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.setWindowProperty(window_name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)


def main_loop(window_name, framerate=100):
    """The ui of the main application flow
    TODO: connect to face detection
    TODO: connect to preprocessed images"""
    block_size = 50
    framerate_calculator = TimeHandler(framerate)
    while True:
        framerate_calculator.reset()
        time_delta = framerate_calculator.get_time_from_start()

        center = (
            np.array((500, 500))
            + 200 * np.array((np.cos(time_delta), np.sin(time_delta)))
        ).astype(int)
        img = np.zeros((1000, 1000, 1))

        img[
            center[0] - block_size : center[0] + block_size,
            center[1] - block_size : center[1] + block_size,
        ] = 255

        cv2.imshow(window_name, img)

        wait_time = framerate_calculator.get_wait_time()

        if wait_time < 1:
            wait_time = 1
        key = cv2.waitKey(wait_time)  # time in milliseconds to wait
        if key == 27:
            break


def application():
    setup(WINDOW_NAME)
    main_loop(WINDOW_NAME)
