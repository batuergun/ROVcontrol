import cv2
import numpy as np
import imutils

class Process:

    def __init__(self, capture_width, capture_height, correctionThreshold):

        self.correctionThreshold = correctionThreshold #(pixels)

        self.capture.set(3, capture_width)
        self.capture.set(4, capture_height)
        
    def findTarget(capture, capture_width, capture_height, correctionThreshold):

        _,frame = capture.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        targetList, targetArea = [], []
        cx, cy = int(capture_width/2), int(capture_height/2)
        cw, ch = capture_width/2, capture_height/2

        #                  lower            upper
        #   Test1   -   [20, 25, 80]   [100, 255, 255]
        #   Test2   -   [50, 50, 100]  [95, 230, 170]

        lower_threshold = np.array([50, 50, 100])     #[20, 25, 80]
        upper_threshold = np.array([95, 230, 170])    #[100, 255, 255]

        mask = cv2.inRange(hsv, lower_threshold, upper_threshold)

        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            area = cv2.contourArea(c)
            if area > 5000:
                targetStatus = 0
                cv2.drawContours(frame, [c], -1, (0, 255, 255), 3)
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                
                if cx < (cw + correctionThreshold) and cx > (cw - correctionThreshold):
                    if cy < (ch + correctionThreshold) and cy > (ch - correctionThreshold):
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

        try: 
            cxMax, cyMax = int(targetList[0][0]), int(targetList[0][1])
            cv2.circle(frame, (cxMax, cyMax), 10, (0, 0, 255), -1)
        except: None

        targetCount = targetList.count()
        for t in targetList:
            xSum = xSum + targetList[t][0]
            ySum = ySum + targetList[t][1]
        
        try: 
            xAverage, yAverage = int(xSum / targetCount), int(ySum / targetCount)
            cv2.circle(frame, (xAverage, yAverage), 10, (200, 50, 0), -1)
        except: None
        
        cv2.circle(frame, (int(cw), int(ch)), correctionThreshold, (255, 255, 255), 1)
        cv2.circle(frame, (int(cw), int(ch)), 2, (255, 255, 255), 2)
        
        cv2.imshow("Test1 Capture", frame)
        return targetList
            

        