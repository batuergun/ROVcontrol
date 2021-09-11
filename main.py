from typing import ForwardRef
from configparser import ConfigParser
import cv2
import threading
import numpy as np
import time

from imageProcess import Process
from Calibration import Calibration
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
            self.capture_width, self.capture_height = 640, 480
            self.correctionThreshold = 50

        if cameraProfile == 1:
            self.drawTargets, self.drawAverage = True, True
            self.capture_width, self.capture_height = 1280, 720
            self.correctionThreshold = 50

        if testProfile == 'config':
            config = ConfigParser()
            config.read('config.ini')
            B_lower = int(config.get('blue', 'lower'))
            B_upper = int(config.get('blue', 'upper'))
            G_lower = int(config.get('green', 'lower'))
            G_upper = int(config.get('green', 'upper'))
            R_lower = int(config.get('red', 'lower'))
            R_upper = int(config.get('red', 'upper'))
            self.lower_threshold = np.array([B_lower, G_lower, R_lower])
            self.upper_threshold = np.array([B_upper, G_upper, R_upper])

        if testProfile == 'live':
            self.lower_threshold = np.array([30, 80, 90])
            self.upper_threshold = np.array([100, 255, 255])
            self.limitMode = [0, 5000, 0]
            self.capture = cv2.VideoCapture(2)

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

        waiting = False
        forward = False
        gateCounter = 0

        startCounter = 5
        forwardCounter = 5

        while True:

            frame = Process(self.lower_threshold, self.upper_threshold, self.correctionThreshold)
            targetList, xAverage, yAverage, image = frame.findTarget(self.capture, self.capture_width, self.capture_height, self.drawTargets, self.drawAverage, self.limitMode)
            
            #640x480

            targetx = xAverage
            xDelta = targetx - 320
            targety = yAverage
            yDelta = targety - 240

            if forward == False:
                if xDelta > 0:
                    xDelta = -xDelta
                    xPWM = Steer._map(xDelta, 0, 320, 0, 10)
                    xPWM = Steer._map(xPWM, 0, 10, 0, -10)
                    #steer.omnidrive(0,0,xPWM,0)

                    if yDelta < 0:
                        yDelta = -yDelta
                        yPWM = Steer._map(yDelta, 0, 240, 0, 10)
                        steer.omnidrive(0,0,xPWM,yPWM)
                    elif yDelta > 0:
                        yPWM = Steer._map(yDelta, 0, 240, 0, 10)
                        yPWM = Steer._map(yPWM, 0, 10, 0, -10)
                        steer.omnidrive(0,0,xPWM,yPWM)

                elif xDelta < 0:
                    xPWM = Steer._map(xDelta, 0, 320, 0, 10)
                    #steer.omnidrive(0,0,x_inverted,0)

                    if yDelta < 0:
                        yDelta = -yDelta
                        yPWM = Steer._map(yDelta, 0, 240, 0, 10)
                        steer.omnidrive(0,0,xPWM,yPWM)
                    elif yDelta > 0:
                        yPWM = Steer._map(yDelta, 0, 240, 0, 10)
                        yPWM = Steer._map(yPWM, 0, 10, 0, -10)
                        steer.omnidrive(0,0,xPWM,yPWM)
                    
                else:
                    steer.hold()
                    xPWM, yPWM = 0, 0
                    start = 0

                if abs(xAverage - 320) < 50 and abs(yAverage - 240) < 50:
                    if xAverage == 320 and yAverage == 240:
                        steer.hold()
                    else:
                        if waiting == False:
                            start = time.time()
                            waiting = True
                        else: 
                            now = time.time()
                            if now - start > startCounter:
                                forward = True
                                steer.omnidrive(0,10,0,0)
            
            else:
                if time.time() - start < forwardCounter + startCounter:
                    steer.omnidrive(0,10,0,0)

                else:
                    forward = False
                    waiting = False
                    gateCounter = gateCounter + 1
            
            #gui.video_stream(image)
            #mask1, mask2 = GUI.getMask()

            interrupt = cv2.waitKey(5)
            if interrupt == 27:
                break
            

if __name__ == '__main__':

    Calibration()
    #rov = ROV(0, 'config')

    #steer = Steer()
    #steer.driveSetup()

    #rov = ROV(0, 'config')
    #ROV.AutonomousDrive(rov)

    #cameraThread = threading.Thread(target=ROVclient.Client.Capture)
    #camera2Thread = threading.Thread(target=ROVclient.Client.Capture2)

    #cameraThread.start()
    #camera2Thread.start()

    #client = ROVclient.Client()
    #client.Connect()

    #steer = Steer()
    #steer.driveSetup()
    #steer.forward(0)
    #time.sleep(10)


    # Manual Control 

    '''
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

    #steer = Steer()
    #Steer.driveSetup(steer)
    #steer.forward(0)
    #time.sleep(3)
    #steer.forward(5)
    #time.sleep(5)

    #steer.stop()

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


    
