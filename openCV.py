#
# import cv2
# import numpy as np
#
# capture = cv2.VideoCapture(0)
#
# while True:
#     ret, im = capture.read()
#
#     im = cv2.bilateralFilter(im, 9, 75, 75)
#     im = cv2.fastNlMeansDenoisingColored(im, None, 10, 10, 7, 21)
#     hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)  # HSV image
#
#     COLOR_MIN = np.array([20, 100, 100], np.uint8)  # HSV color code lower and upper bounds
#     COLOR_MAX = np.array([30, 255, 255], np.uint8)  # color yellow
#
#     frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)  # Thresholding image
#     imgray = frame_threshed
#     ret, thresh = cv2.threshold(frame_threshed, 127, 255, 0)
#     im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     type(contours)
#     for cnt in contours:
#         x, y, w, h = cv2.boundingRect(cnt)
#         cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     cv2.imshow("Show", im)
#
#
# cv2.destroyAllWindows()

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)

    edges = cv2.Canny(frame, 100, 200)

    cv2.imshow('edges', edges)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('maks', mask)
    cv2.imshow('res', res)



    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 2)

    im2, contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (255, 255, 0), 3)
    cv2.imshow("Keypoints", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

