import cv2
import cv2 as cv
import math
import numpy as np
from functools import cmp_to_key as c2k
import traceback

cap = cv.VideoCapture(0)


@c2k
def sort_by_x(point_1, point_2):
    return point_1[0] < point_2[0]


@c2k
def sort_by_y(point_1, point_2):
    return point_1[1] < point_2[1]


COLORS = {"WHITE": [179, 179, 171],
          "BLUE": [125, 76, 22],
          "YELLOW": [85, 153, 169],
          "GREEN": [62, 87, 15],
          "ORANGE": [62, 100, 171],
          "RED": [53, 53, 140]}

faces = [[],[],[],[],[],[]]
keys = ["WHITE", "BLUE", "RED", "YELLOW", "ORANGE", "GREEN"]

request_confirm = False
index = 0
while index != 6:
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

    if len(rects) == 9:

        for n, k in enumerate(rects):
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
        cube = [[], [], []]

        miny = 99999

        maxy = 0

        for n, c in enumerate(rectcentroid):
            miny = min(miny, c[1])
            maxy = max(maxy, c[1])

        for n, c in enumerate(rectcentroid):
            if abs(miny - c[1]) < 30:
                cube[0].append(c)
            elif abs(maxy - c[1]) < 30:
                cube[2].append(c)
            else:
                cube[1].append(c)

        for n, row in enumerate(cube):
            cube[n] = sorted(row)

        colors = []

        for y in range(3):
            for x in range(3):
                try:
                    cv.putText(frame, str(y*3+x), tuple(cube[y][x][:2]), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    mask = np.zeros(frame.shape[:2], np.uint8)
                    cv.drawContours(mask, [cube[y][x][2]], 0, 255, -1)
                    mean_val = cv.mean(frame, mask=mask)

                    color = mean_val

                    cv.drawContours(frame, [cube[y][x][2]], -1, tuple(color), 2)

                    for key in COLORS.keys():
                        c = COLORS[key]
                        correct = True
                        for n, channel in enumerate(c):
                            if abs(channel - mean_val[n]) > 30:
                                correct = False

                        if correct:
                            cube[y][x] = key
                            break
                        else:
                            cube[y][x] = False
                except:
                    pass

        match_complete = True

        for y in range(len(cube)):
            for x in range(len(cube[y])):
                if not cube[y][x]:
                    match_complete = False
            if not match_complete:
                break

        if match_complete:
            if cube[1][1] == keys[index]:
                if request_confirm and cube == faces[index]:
                    index += 1
                    request_confirm = False
                    print(keys[index - 1] + " done!")
                else:
                    faces[index] = cube
                    request_confirm = True

        print(faces)
        if index != 6:
            print(keys[index])
        for row in cube:
            print(row)
        print()

        rects = np.array(rects)

        cv2.imshow('contours', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

print(faces)
