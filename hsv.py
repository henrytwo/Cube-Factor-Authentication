import cv2
import numpy as np

cap = cv2.VideoCapture(0)

FOV = 62.52
W = 520
H = 320

while (1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([20, 100, 100])
    upper_red = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    # res = cv2.bitwise_and(frame,frame, mask= mask)

    im2, cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]

    # print(cnts)

    rects = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        if h >= 40 and w >= 40:
            print(FOV * (x - W // 2) / W, y - H // 2)

            # if height is enough
            # create rectangle for bounding
            rect = (x, y, w, h)
            rects.append(rect)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1);

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()