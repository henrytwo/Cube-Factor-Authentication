#
# import cv
# import numpy as np
#
# capture = cv.VideoCapture(0)
#
# while True:
#     ret, im = capture.read()
#
#     im = cv.bilateralFilter(im, 9, 75, 75)
#     im = cv.fastNlMeansDenoisingColored(im, None, 10, 10, 7, 21)
#     hsv_img = cv.cvtColor(im, cv.COLOR_BGR2HSV)  # HSV image
#
#     COLOR_MIN = np.array([20, 100, 100], np.uint8)  # HSV color code lower and upper bounds
#     COLOR_MAX = np.array([30, 255, 255], np.uint8)  # color yellow
#
#     frame_threshed = cv.inRange(hsv_img, COLOR_MIN, COLOR_MAX)  # Thresholding image
#     imgray = frame_threshed
#     ret, thresh = cv.threshold(frame_threshed, 127, 255, 0)
#     im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#
#     type(contours)
#     for cnt in contours:
#         x, y, w, h = cv.boundingRect(cnt)
#         cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     cv.imshow("Show", im)
#
#
# cv.destroyAllWindows()

import numpy as np
import cv2 as cv

cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv.CAP_PROP_EXPOSURE, 0.1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv.imshow('Main', frame)

    edges = cv.Canny(frame, 100, 200)

    # cv.imshow('edges', edges)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    blue_res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('Blue', blue_res)

    # lower_green = np.array([60, 50, 50])
    # upper_green = np.array([80, 255, 255])

    lower_orange = np.array([0, 50, 150])
    upper_orange = np.array([20, 255, 255])
    mask = cv.inRange(hsv, lower_orange, upper_orange)
    orange_res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('Orange', orange_res)

    lower_yellow = np.array([44, 85, 75])
    upper_yellow = np.array([35, 75, 100])
    mask = cv.inRange(hsv, lower_yellow, upper_yellow)
    yellow_res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('Yellow', yellow_res)

    imgray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    th3 = cv.adaptiveThreshold(
        imgray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 51, 2)

    im2, contours, hierarchy = cv.findContours(
        th3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(frame, contours, -1, (255, 255, 0), 3)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
