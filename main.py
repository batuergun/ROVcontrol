import cv2

from imageProcess import Process
from ROVdrive import Steer
#from droneClient import TcpClient

#class ROV:

    #def __init__(self):

    #def main(self):


if __name__ == '__main__':

    capture = cv2.VideoCapture("A:/Ubuntu/Projects/gateRecognition/test1.mp4")
    capture_width, capture_height = 1280, 720
    correctionThreshold = 50

    while True:
        targetList = Process.findTarget(capture, capture_width, capture_height, correctionThreshold)
        
        target = Steer(targetList)
        Steer.targetEvaluation(targetList)

        interrupt = cv2.waitKey(5)
        if interrupt == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
