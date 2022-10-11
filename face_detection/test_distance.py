from distance import *

cap = cv2.VideoCapture(0)
i = 0
# let distance array default to known width
distance_array = np.ones(24) * 60
while True:
    _, frame = cap.read()
    angle, distance_array = get_angle_from_frame(
        frame, i=i, distance_array=distance_array
    )
    i += 1
    print(angle)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
