from distance import get_angle_from_frame, Focal_Length_Finder
import cv2
import numpy as np

"""
test_distance.py

Example on how to use distance.py
"""
# real life distance
Known_distance = 72  # 66

# width of face in the real world or Object Plane
# centimeter
Known_width = 15
# find focal length
Focal_length = Focal_Length_Finder(
    Known_distance,
    Known_width,
)
cap = cv2.VideoCapture(0)
i = 0
# let distance array default to known width
distance_array = np.ones(24) * 60
while True:
    _, frame = cap.read()
    angle, distance_array = get_angle_from_frame(
        frame, Focal_length, i=i, distance_array=distance_array
    )
    i += 1
    print(angle)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
