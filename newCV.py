import cv2
import cv2 as cv
import math
import numpy as np

cap = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv.imshow('Main', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 20, 40)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=2)

    img2, contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        maxlen = -1
        maxdiff = 0
        ld = []

        if len(approx) == 4 and 8000 > cv2.contourArea(c) > 2000:

            for k in range(3):
                ld.append(math.hypot(approx[k][0][0] - approx[k+1][0][0], approx[k][0][1] - approx[k+1][0][1]))
            ld.append(math.hypot(approx[0][0][0] - approx[3][0][0], approx[0][0][1] - approx[3][0][1]))

            maxdiff = max([abs(ld[x] - ld[x+1]) for x in range(3)] + [abs(ld[0] - ld[2])])

            M = cv.moments(c)

            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            if maxdiff < 30:
                rects.append(approx)



    rects = np.array(rects)

    cv2.drawContours(frame, rects, -1, (255,255,255), 1)

    cv2.imshow('contours', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
