import cv2
import numpy as np
import time
import soninsik as htm

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
drawColor = (255,255,255)
brushThickness = 10

detector = htm.handDetector(detectionCon = 0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)

    if len(lmList) != 0:
        # print(lmList)

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        # print(fingers)

        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1-15), (x2, y2+25), drawColor, cv2.FILLED)
            # print("notdraw")
            xp, yp = 0, 0

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("draw")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

        if fingers[1] and fingers[2] and fingers[3]:
            if drawColor == (255,255,255):
                drawColor = (0,0,0)
                brushThickness = 60
            else:
                drawColor = (255,255,255)
                brushThickness = 10

        if all (x >= 1 for x in fingers):
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)
            print('clear')
            drawColor = (255, 255, 255)
            brushThickness = 10

    cv2.imshow("Image", imgCanvas)
    cv2.waitKey(1)

