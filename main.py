import cv2
import threading
import numpy as np
import time

from imageProcess import Process
from gui import GUI
from ROVdrive import Steer
import ROVclient

class ROV:
    def __init__(self, cameraProfile, testProfile):

        self.cameraThread = threading.Thread(target=ROVclient.Client.Capture)
        #self.driveThread = threading.Thread(target=Client.old_drive)

        #                  lower            upper               limitMode
        #   Test1   -   [50, 50, 100]  [95, 230, 170]       [0, 5000, 0]        (Initial test)
        #   Test2   -   [20, 25, 80]   [100, 255, 255]      [0, 5000, 0]        (Render Data)
        #   Test3   -   [80, 80, 100]  [99, 130, 255]       [1, 4000, 40000]    (Pool #2)
        #   Test4   -   [30, 90, 170]  [220, 255, 255]      [0, 5000, 0]        (Live Feed)

        if cameraProfile == 0:
            self.drawTargets, self.drawAverage = True, True
            self.capture_width, self.capture_height = 480, 360
            self.correctionThreshold = 50

        if testProfile == 'live':
            self.lower_threshold = np.array([30, 90, 170])
            self.upper_threshold = np.array([220, 255, 255])
            self.limitMode = [0, 5000, 0]
            #self.capture = cv2.VideoCapture(0) 

        if testProfile == 1:
            self.lower_threshold = np.array([50, 50, 100])
            self.upper_threshold = np.array([95, 230, 170])
            self.limitMode = [0, 5000, 0]
            self.capture = cv2.VideoCapture("/home/pi/Desktop/pi/test1.mp4")

        if testProfile == 2:
            self.lower_threshold = np.array([20, 25, 80])
            self.upper_threshold = np.array([100, 255, 255])
            self.limitMode = [0, 5000, 0]
            self.capture = cv2.VideoCapture("/home/pi/Desktop/pi/test1.mp4")

        if testProfile == 3:
            self.lower_threshold = np.array([80, 80, 100])
            self.upper_threshold = np.array([99, 130, 255])
            self.limitMode = [1, 4000, 40000]
            self.capture = cv2.VideoCapture("/home/pi/Desktop/pi/test1.mp4")
            

    def AutonomousDrive(self):

        while True:
            frame = Process(self.lower_threshold, self.upper_threshold, self.correctionThreshold)
            targetList, customTargets = frame.findTarget(self.capture, self.capture_width, self.capture_height, self.drawTargets, self.drawAverage, self.limitMode)
            #GUI(self.capture)
            
            t = Steer()
            Steer.targetEvaluation(targetList)

            interrupt = cv2.waitKey(5)
            if interrupt == 27:
                break
            
        self.capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':

    #rov = ROV(0, 'live')
    #ROV.AutonomousDrive(rov)

    cameraThread = threading.Thread(target=ROVclient.Client.Capture)
    camera2Thread = threading.Thread(target=ROVclient.Client.Capture2)

    cameraThread.start()
    camera2Thread.start()

    client = ROVclient.Client()
    client.Connect()

    steer = Steer()
    #steer.driveSetup()
    steer.forward(0)
    time.sleep(3)

    while True:
        joystick = ROVclient.Client.driveRuntime()
        joystickAxis = joystick.split('.')
        
        axis = [0, 0, 0, 0, 0, 0]
        axis[0] = int(float(joystickAxis[0]))
        axis[1] = int(joystickAxis[1])
        axis[2] = int(joystickAxis[2])
        axis[3] = int(joystickAxis[3])
        axis[4] = int(joystickAxis[4])
        axis[5] = int(joystickAxis[5])

        if axis[5] > 0:
            steer.rotate(axis[5], 'left')
        elif axis[4] > 0:
            steer.rotate(axis[4], 'right')
        else:
            steer.omnidrive(axis[0],axis[1],axis[2],axis[3])

        print(axis)
        '''
        if axis[2] > 0 or axis[3] > 0:
            steer.omnidirectional(axis[2], axis[3])

        elif axis[2] < 0 or axis[3] < 0:
            steer.omnidirectional(axis[2], axis[3])

        elif axis[0] > 0 or axis[1] > 0:
            steer.eulerRotate(axis[0], axis[1])
        
        elif axis[0] < 0 or axis[1] < 0:
            steer.eulerRotate(axis[0], axis[1])

        else:
            steer.hold()

        '''
        #print(axis)
        
        #steer.turn(int(axis[0]))

    #steer = Steer()
    #Steer.driveSetup(steer)
    #steer.forward(0)
    #time.sleep(3)
    #steer.forward(5)
    #time.sleep(5)

    #steer.stop()


    
