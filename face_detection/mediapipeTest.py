import cv2
import mediapipe as mp
import numpy as np
import itertools


GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def get_facemesh_coords(face_landmarks, img):

    RIGHT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_IRIS)))

    eye_landmark = face_landmarks.landmark[RIGHT_EYE_INDEXES[0]]
    """Extract FaceMesh landmark coordinates into 468x3 NumPy array."""
    h, w = img.shape[:2]  # grab width and height from image
    xyz = np.array([eye_landmark.x, eye_landmark.y, eye_landmark.z])

    return xyz  # np.multiply(xyz, [w, h, w]).astype(int)


def draw_mediapipe_facedetect():
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

                # pos_right = mp_face_detection.get_key_point(detection, 4)
                # pos_left = mp_face_detection.get_key_point(detection, 5)

                # distance = pos_left.x - pos_right.x

                cv2.putText(
                    image,
                    f"distance: {round(distance, 2)}",
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


def draw_mediapipe_face_mesh():
    # For webcam input:
    cap = cv2.VideoCapture(0)
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as face_mesh:
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
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                    )
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
                    )
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style(),
                    )
                    coords = get_facemesh_coords(face_landmarks, image)
                cv2.putText(
                    image,
                    f"angle: {round(coords[0], 2)}",
                    (400, 35),
                    fonts,
                    0.6,
                    BLACK,
                    2,
                )
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow("MediaPipe Face Mesh", image)
            if cv2.waitKey(1) == ord("q"):
                break
    cap.release()


class face_mesh_obj:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.coords = np.zeros(3)

    def close(self):
        if cv2.waitKey(1) == ord("q"):
            self.cap.release()

    def detect_face(self):
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as face_mesh:
            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("ignoring empty frame")
                    continue
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        self.coords = get_facemesh_coords(face_landmarks, image)
                cv2.imshow("face mesh", image)
                yield self.coords
                self.close()


if __name__ == "__main__":
    # for demostration purposes, get drawing of face-grid
    draw_mediapipe_face_mesh()

    # test with object, get coordniates out while doing video-capturing
    # fmObj = face_mesh_obj()
    # for coords in fmObj.detect_face():
    #     print(coords[0])
