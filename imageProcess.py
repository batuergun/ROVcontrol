import cv2
import numpy as np
import imutils

class Process:

    def __init__(self):

        self.correctionThreshold = 20 #(pixels)

        capture = cv2.VideoCapture("A:/Ubuntu/Projects/gateRecognition/test1.mp4")
        capture_width, capture_height = 1280, 720

        capture.set(3, capture_width)
        capture.set(4, capture_height)
        
    def findTarget(self):

        while True:
            _,frame = self.capture.read()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            #                  lower            upper
            #   Test1   -   [20, 25, 80]   [100, 255, 255]
            #   Test2   -   [50, 50, 100]  [95, 230, 170]

            lower_threshold = np.array([50, 50, 100])     #[20, 25, 80]
            upper_threshold = np.array([95, 230, 170])    #[100, 255, 255]

            mask = cv2.inRange(hsv, lower_threshold, upper_threshold)

            contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            cw, ch = self.capture_width/2, self.capture_height/2
            cv2.circle(frame, (int(cw), int(ch)), self.correctionThreshold, (255, 255, 255), 1)
            cv2.circle(frame, (int(cw), int(ch)), 2, (255, 255, 255), 2)

            for c in contours:
                area = cv2.contourArea(c)
                if area > 5000:
                    cv2.drawContours(frame, [c], -1, (0, 255, 255), 3)
                    M = cv2.moments(c)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
                    cv2.line(frame, (int(cw), int(ch)), (cx, cy), (50, 255, 0), 1)
                    #cv2.putText(frame, "Gate", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)

            
            cv2.imshow("Test1 Capture", frame)
            k = cv2.waitKey(5)
            if k == 27:
                break

        self.capture.release()
        cv2.destroyAllWindows()