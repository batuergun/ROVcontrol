import cv2
import numpy as np

from imageProcess import Process
from ROVdrive import Steer

class ROV:
    def __init__(self, driveSpeed):
        self.driveSpeed = driveSpeed

    def AutonomousDrive():
        
        #                  lower            upper
        #   Test1   -   [20, 25, 80]   [100, 255, 255]
        #   Test2   -   [50, 50, 100]  [95, 230, 170]

        lower_threshold = np.array([50, 50, 100])     #[20, 25, 80]
        upper_threshold = np.array([95, 230, 170])    #[100, 255, 255]

        capture = cv2.VideoCapture("A:/Ubuntu/Projects/gateRecognition/test1.mp4")
        capture_width, capture_height = 1280, 720
        correctionThreshold = 50
        drawTargets, drawAverage = True, True

        while True:
            frame = Process(lower_threshold, upper_threshold, correctionThreshold)
            targetList, customTargets = frame.findTarget(capture, capture_width, capture_height, drawTargets, drawAverage)
            
            target = Steer(targetList)
            Steer.targetEvaluation(targetList)

            interrupt = cv2.waitKey(5)
            if interrupt == 27:
                break
            
        capture.release()
        cv2.destroyAllWindows()
    
#    def ManualDrive():


if __name__ == '__main__':

    ROV.AutonomousDrive()
