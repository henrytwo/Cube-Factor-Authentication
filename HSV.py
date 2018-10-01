import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (1, 1), 0)

    img2, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(frame.shape[:2], np.uint8)
    cv2.drawContours(mask, contours, 0, 255, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)

    try:
        print(str(frame[min_loc]))
        print(str(frame[max_loc]))

        cv2.putText(frame, str(frame[min_loc]), min_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, str(frame[max_loc]), max_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("frame", frame)
        cv2.imshow("gray", gray)
        cv2.imshow("mask", mask)
    except:
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()



