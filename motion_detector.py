import cv2

first_frame = None

webcam = cv2.VideoCapture(0)  # using internal webcam

while True:
    check, frame = webcam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if first_frame is None:
        first_frame = gray  # get the grayscale image which represents the very first frame of the webcam
    cv2.imshow("Capturing", gray)

    key = cv2.waitKey(1)
    print(gray)

    if key == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
