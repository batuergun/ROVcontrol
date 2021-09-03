import cv2
import numpy as np
import imutils

class Process:

    def __init__(self, lower_threshold, upper_threshold, correctionThreshold):

        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.correctionThreshold = correctionThreshold

        
    def findTarget(self, capture, capture_width, capture_height, drawTargets, drawAverage):

        _,frame = capture.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        targetList, customTargets = [], []
        cx, cy = int(capture_width/2), int(capture_height/2)
        cw, ch = capture_width/2, capture_height/2

        mask = cv2.inRange(hsv, self.lower_threshold, self.upper_threshold)

        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            area = cv2.contourArea(c)
            if area > 5000 and area < 15000:
                targetStatus = 0
                cv2.drawContours(frame, [c], -1, (0, 255, 255), 3)
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                
                if cx < (cw + self.correctionThreshold) and cx > (cw - self.correctionThreshold):
                    if cy < (ch + self.correctionThreshold) and cy > (ch - self.correctionThreshold):
                        cv2.circle(frame, (cx, cy), 7, (0, 255, 0), -1)
                        targetStatus = 1
                    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
                else:
                    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

                cv2.line(frame, (int(cw), int(ch)), (cx, cy), (50, 255, 0), 1)
                #cv2.putText(frame, "Gate", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)

                targetList.append((cx, cy, area, targetStatus))

        targetList.sort(key=lambda x: int(x[2]))
        targetList.reverse()

        cv2.circle(frame, (int(cw), int(ch)), self.correctionThreshold, (255, 255, 255), 1)
        cv2.circle(frame, (int(cw), int(ch)), 2, (255, 255, 255), 2)
        
        if drawTargets == True:
            try: 
                cxMax, cyMax = int(targetList[0][0]), int(targetList[0][1])
                cv2.circle(frame, (cxMax, cyMax), 10, (0, 0, 255), -1)
            except: None

        if drawAverage == True:
            xSum, ySum = 0, 0
            targetCount = len(targetList)
            for t in range(0, targetCount):
                xBuffer, yBuffer = int(targetList[t][0]), int(targetList[t][1])
                xSum = xSum + xBuffer
                ySum = ySum + yBuffer

            try: 
                xAverage, yAverage = int(xSum / targetCount), int(ySum / targetCount)
                cv2.circle(frame, (xAverage, yAverage), 10, (200, 50, 0), -1)
            except: None

        try: customTargets.append((cxMax, cyMax, xAverage, yAverage))
        except: customTargets = []

        cv2.imshow("Test1 Capture", frame)
        return targetList, customTargets