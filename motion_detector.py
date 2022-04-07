from datetime import datetime

import time
import cv2
import pandas
import warnings
# avoid the FutureWarning that 'frame.append method is deprecated and will be removed from pandas in a future version' when executing
warnings.simplefilter(action='ignore', category=FutureWarning)


first_frame = None
status_list = [None, None]  # avoid IndexError when execute line 44
times = []
data_frame = pandas.DataFrame(columns=["Start", "End"])

webcam = cv2.VideoCapture(0)  # 0 to use internal webcam
# to avoid IndexError that may happen in times in line 71 due to times has an odd number of elements
# wait more than 2s delay that's been prefixed before bring moving object into camera's view
webcam.read()
time.sleep(1)

while True:
    check, frame = webcam.read()
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blur the image to make it smooth
    # because that removes noise and increases accuracy in the calculation of the difference

    if first_frame is None:
        first_frame = gray  # get the grayscale image which represents the very first frame of the webcam
        continue  # means continue to the beginning of the loop and don't go all around the rest of the code.
        # after starting the next iteration, first_frame is not None anymore
        # therefor after executing line 27, line 36 will be executed next

    delta_frame = cv2.absdiff(first_frame, gray)  # the result of comparing two blurred grayscale images = new image
    thresh_frame = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        status = 1  # object enters to frame, change status to one

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    status_list.append(status)

    if len(status_list) > 2:
        # record the status when changing from 1 to 0 and vice verse
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())
        if status_list[-1] == 0 and status_list[-2] == 1:
            times.append(datetime.now())

    status_list = status_list[-2:]  # to save memory

    # cv2.imshow("Gray Frame", gray)
    # cv2.imshow("Delta Frame", delta_frame)
    # cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    print(gray)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    data_frame = data_frame.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

data_frame.to_csv("Times.csv")
webcam.release()
cv2.destroyAllWindows()
