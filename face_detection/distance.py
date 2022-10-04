# install opencv "pip install opencv-python"
import cv2
import numpy as np

# distance from camera to object(face) measured
# centimeter
Known_distance = 72  # 66

# width of face in the real world or Object Plane
# centimeter
Known_width = 15

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

# face detector object
face_detector = cv2.CascadeClassifier(
    "..\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml"
)

# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):

    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):

    distance = (real_face_width * Focal_Length) / face_width_in_frame

    # return the distance
    return distance


def calculate_angle(distance, Focal_Length, X, Y):
    K = np.array([[Focal_Length, 0, 640], [0, Focal_Length, 512], [0, 0, 1]])
    P = np.array([X, Y, distance])
    p = K.dot(P)
    x, y = p[0] / p[2], p[1] / p[2]

    Ki = np.linalg.inv(K)
    r1 = Ki.dot([x, y, 1.0])
    r2 = Ki.dot([x, y, 2.0])

    cos_angle = r1.dot(r2) / (np.linalg.norm(r1) * np.linalg.norm(r2))
    angle = np.arccos(cos_angle) * 180 / np.pi

    # normalize the angle
    angle = (angle - 7) / (21 - 7)

    return angle


def face_data(image):

    face_width = 0  # making face width to zero

    # converting color image to gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    x = 0
    y = 0
    w = 0
    h = 0
    for (x, y, h, w) in faces:

        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width, x + w / 2, y + h / 2


# reading reference_image from directory
ref_image = cv2.imread("testImage2.jpg")

# find the face width(pixels) in the reference_image
ref_image_face_width, x, y = face_data(ref_image)

# get the focal by calling "Focal_Length_Finder"
# face width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width
)

print(Focal_length_found)

# show the reference image
cv2.imshow("ref_image", ref_image)

# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture(0)

# looping through frame, incoming from
# camera/video

distance_array = np.zeros(24)
i = 0
while True:

    # reading the frame from camera
    _, frame = cap.read()

    # calling face_data function to find
    # the width of face(pixels) in the frame
    face_width_in_frame, x, y = face_data(frame)

    # check if the face is zero then not
    # find the distance
    if face_width_in_frame != 0:

        # finding the distance by calling function
        # Distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
        Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)
        distance_array[i] = Distance - 20
        # draw line as background of text
        cv2.line(frame, (30, 30), (230, 30), RED, 32)
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

        # Drawing Text on the screen
        mean_dist = np.mean(distance_array)
        if i == len(distance_array) - 1:
            i = 0

        angle = calculate_angle(mean_dist, Focal_length_found, x, y)

        cv2.putText(
            frame,
            f"Distance: {round(mean_dist,0)} CM",
            (30, 35),
            fonts,
            0.6,
            GREEN,
            2,
        )
        cv2.putText(
            frame,
            f"Angle: {round(angle,3)}",
            (400, 35),
            fonts,
            0.6,
            GREEN,
            2,
        )
        i += 1

    # show the frame on the screen
    cv2.imshow("frame", frame)

    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break

# closing the camera
cap.release()

# closing the windows that are opened
cv2.destroyAllWindows()
