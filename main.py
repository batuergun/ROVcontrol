import cv2
import numpy as np

from imageProcess import Process
from ROVdrive import Steer

class ROV:
    def __init__(self, id):
        self.id = id

    def AutonomousDrive():
        
        #                  lower            upper               limitMode
        #   Test1   -   [50, 50, 100]  [95, 230, 170]       [0, 5000, 0]        (Initial test)
        #   Test2   -   [20, 25, 80]   [100, 255, 255]      [0, 5000, 0]        (Render Data)
        #   Test3   -   [80, 80, 100]  [99, 130, 255]       [1, 4000, 40000]    (Pool #2)
        #   Test4   -   [30, 90, 170]  [220, 255, 255]      [0, 5000, 0]        (Live Feed)

        lower_threshold = np.array([80, 80, 100])
        upper_threshold = np.array([99, 130, 255])

        capture = cv2.VideoCapture("A:/Ubuntu/Projects/gateRecognition/test3.mp4")
        limitMode = [1, 4000, 40000]

        capture_width, capture_height = 1280, 720
        correctionThreshold = 50
        
        drawTargets, drawAverage = True, True

        while True:
            frame = Process(lower_threshold, upper_threshold, correctionThreshold)
            targetList, customTargets = frame.findTarget(capture, capture_width, capture_height, drawTargets, drawAverage, limitMode)
            
            t = Steer(targetList)
            Steer.targetEvaluation(targetList)

            interrupt = cv2.waitKey(5)
            if interrupt == 27:
                break
            
        capture.release()
        cv2.destroyAllWindows()
    
#    def ManualDrive():


if __name__ == '__main__':

    ROV.AutonomousDrive()
