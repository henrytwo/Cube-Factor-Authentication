import cv2
import cv2 as cv
import math
import numpy as np
from functools import cmp_to_key as c2k

cap = cv.VideoCapture(0)


@c2k
def sort_by_x(point_1, point_2):
    return point_1[0] - point_1[0] - point_2[0] > 30


@c2k
def sort_by_y(point_1, point_2):
    return point_1[1] < point_2[1]


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
    rectcentroid = []
    maxcont = []
    maxsize = 0

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        maxlen = -1
        maxdiff = 0
        ld = []

        if len(approx) == 4:

            for k in range(3):
                ld.append(math.hypot(approx[k][0][0] - approx[k + 1][0][0], approx[k][0][1] - approx[k + 1][0][1]))
            ld.append(math.hypot(approx[0][0][0] - approx[3][0][0], approx[0][0][1] - approx[3][0][1]))

            maxdiff = max([abs(ld[x] - ld[x + 1]) for x in range(3)] + [abs(ld[0] - ld[2])])

            M = cv.moments(c)

            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            if maxdiff < 30:
                if 8000 > cv2.contourArea(c) > 2000:
                    rectcentroid.append((cx, cy))
                    rects.append(approx)
    tremove = []

    for j in range(len(rects)):
        for k in range(j + 1, len(rects)):
            if cv2.pointPolygonTest(rects[j], rectcentroid[k], True) > 0:
                if cv2.contourArea(rects[j]) > cv2.contourArea(rects[k]):
                    tremove.append(rects[j])
                else:
                    tremove.append(rects[k])

    for r in tremove:
        for k in range(len(rects)):
            if np.array_equal(r, rects[k]):
                del rects[k]
                break

    rectcentroid = []

    for k in rects:
        M = cv.moments(k)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        rectcentroid.append([cx, cy, k])

    sorted_centroids = []

    # sorted_x = sorted(rectcentroid, key=sort_by_x)
    # for centroids in [sorted_x[i:i + 3] for i in range(0, len(rectcentroid), 3)]:
    #     sorted_y = sorted(centroids, key=sort_by_y)
    #     sorted_centroids.extend(sorted_y)
    #
    # for n, s in enumerate(sorted_centroids):
    #     cv.putText(frame, str(n), tuple(s[:2]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    colors = []

    for k in sorted_centroids:
        try:
            colors.append(frame[k[0]][k[1]])
        except:
            pass
    print(len(colors))
    print(colors)

    rects = np.array(rects)

    cv2.drawContours(frame, rects, -1, (255, 255, 255), 1)

    cv2.imshow('contours', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
