import cv2
import mediapipe as mp
import numpy as np
import itertools
import time

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FaceMesh constants
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_FACES = 1


# Screen text constants
X_ANGLE_X_COORD = 400
X_ANGLE_Y_COORD = 35
Y_ANGLE_X_COORD = 400
Y_ANGLE_Y_COORD = 80
FPS_X_COORD = 100
FPS_Y_COORD = 35

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# coordinate constant
RIGHT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_IRIS)))


def get_facemesh_coords(face_landmarks, img):

    eye_landmark = face_landmarks.landmark[RIGHT_EYE_INDEXES[0]]
    """Extract FaceMesh landmark coordinates into 468x3 NumPy array."""
    h, w = img.shape[:2]  # grab width and height from image
    xyz = np.array([eye_landmark.x, eye_landmark.y, eye_landmark.z])

    return xyz  # np.multiply(xyz, [w, h, w]).astype(int)


def draw_mediapipe_face_mesh():
    # For webcam input:
    cap = cv2.VideoCapture(0)
    fps_list = []
    mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    with mp_face_mesh.FaceMesh(
        max_num_faces=MAX_NUM_FACES,
        refine_landmarks=True,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    ) as face_mesh:
        while cap.isOpened():
            t_start = time.time()
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
                    f"x: {round(coords[0], 2)}",
                    (X_ANGLE_X_COORD, X_ANGLE_Y_COORD),
                    fonts,
                    0.6,
                    BLACK,
                    2,
                )
                cv2.putText(
                    image,
                    f"y: {round(coords[1], 2)}",
                    (Y_ANGLE_X_COORD, Y_ANGLE_Y_COORD),
                    fonts,
                    0.6,
                    BLACK,
                    2,
                )
            fps_list.append(1 / (time.time() - t_start))
            cv2.putText(
                image,
                f"fps: {round(np.mean(fps_list),2)}",
                (FPS_X_COORD, FPS_Y_COORD),
                fonts,
                0.6,
                BLACK,
                2,
            )
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow("MediaPipe Face Mesh", image)
            if cv2.waitKey(1) == ord("q"):
                print(len(fps_list))
                break
    cap.release()


class FaceMeshObj:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.coords = np.zeros(3)

    def close(self):
        if cv2.waitKey(1) == ord("q"):
            self.cap.release()

    def detect_face(self):
        with mp_face_mesh.FaceMesh(
            max_num_faces=MAX_NUM_FACES,
            refine_landmarks=True,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
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
                yield self.coords
                self.close()


if __name__ == "__main__":
    demo = True
    # for demostration purposes, get drawing of face-grid
    if demo:
        draw_mediapipe_face_mesh()
    else:
        # test with object, get coordniates out while doing video-capturing
        fmObj = FaceMeshObj()
        for coords in fmObj.detect_face():
            print(coords[0])
