import cv2
import mediapipe as mp
import numpy as np


GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=1
) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            min_dist = -np.inf
            for detection in results.detections:
                pos_right = mp_face_detection.get_key_point(detection, 4)
                pos_left = mp_face_detection.get_key_point(detection, 5)

                distance = pos_left.x - pos_right.x
                if distance > min_dist:
                    min_dist = distance
                    mp_drawing.draw_detection(image, detection)

            # Flip the image horizontally for a selfie-view display.
            pos_right = mp_face_detection.get_key_point(detection, 4)
            pos_left = mp_face_detection.get_key_point(detection, 5)

            distance = pos_left.x - pos_right.x

            cv2.putText(
                image,
                f"Angle: {round(distance, 2)}",
                (400, 35),
                fonts,
                0.6,
                GREEN,
                2,
            )
        cv2.imshow("MediaPipe Face Detection", image)
        if cv2.waitKey(1) == ord("q"):
            break
cap.release()
