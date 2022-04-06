import cv2

first_frame = None

webcam = cv2.VideoCapture(0)  # using internal webcam

while True:
    check, frame = webcam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blur the image to make it smooth
    # because that removes noise and increases accuracy in the calculation of the difference

    if first_frame is None:
        first_frame = gray  # get the grayscale image which represents the very first frame of the webcam
        continue  # means continue to the beginning of the loop and don't go all around the rest of the code.
        # after the next iteration, first_frame is not None anymore
        # therefor after executed line 11, line 20 will be executed next

    delta_frame = cv2.absdiff(first_frame, gray)  # the result of comparing two blurred grayscale images = new image
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    # cv2.imshow("Gray Frame", gray)
    # cv2.imshow("Delta Frame", delta_frame)
    # cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    print(gray)

    if key == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
