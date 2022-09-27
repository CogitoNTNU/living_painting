import cv2

cascPathEye = "..\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml"
cascPathFace = (
    "..\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt2.xml"
)
cascPathProfile = "..\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_profileface.xml"

faceCascade = cv2.CascadeClassifier(cascPathFace)
eyeCascade = cv2.CascadeClassifier(cascPathEye)
profilaCascade = cv2.CascadeClassifier(cascPathProfile)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    profile = profilaCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(x, y)

    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(x, y)

    for (x, y, w, h) in profile:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(x, y)

    # Display the resulting frame
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
