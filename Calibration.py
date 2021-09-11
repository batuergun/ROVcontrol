from configparser import ConfigParser
from tkinter import *
import tkinter
import cv2
from PIL import ImageTk, Image

import numpy as np
import imutils

class Calibration:

    def __init__(self):

        capture_width, capture_height = 1280, 720
        correctionThreshold = 50
        limitMode = [0, 5000, 0]

        lower_threshold = np.array([30, 80, 90])
        upper_threshold = np.array([100, 255, 255])

        # Limit mode 0 -> [0, areaMinThreshold, None]
        # Limit mode 1 -> [1, areaMinThreshold, areaMaxThreshold]

        Calibration.getConfig(self)
        
        self.window = Tk()
        self.window.title('ROVControl')
        self.window.geometry('1280x750')

        top = Frame(self.window, padx=10, pady=10)
        top.pack()

        ControlPanel = Frame(top, padx=10, pady=10, width=400, height=240)
        ControlPanel.pack(side=LEFT)

        # Camera 1 Setup
        Camera1 = Frame(top, padx=10, pady=10, bg='#2aaad1', width=800, height=480)

        lmain = Label(Camera1)
        lmain.pack()

        self.cap = cv2.VideoCapture(0)

        def findCenter(self, c, frame, capture_width, capture_height):
            cx, cy = int(capture_width/2), int(capture_height/2)
            cw, ch = capture_width/2, capture_height/2
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
            return cx, cy, targetStatus

        def video_stream():
            targetList, customTargets = [], []
            cw, ch = capture_width/2, capture_height/2

            _,frame = self.cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_threshold, upper_threshold)
            contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            for c in contours:
                area = cv2.contourArea(c)
                if limitMode[0] == 0:
                    if area > limitMode[1]:
                        cx, cy, targetStatus = findCenter(self, c, frame, capture_width, capture_height)
                        targetList.append((cx, cy, area, targetStatus))
                if limitMode[0] == 1:
                    if area > limitMode[1] and area < limitMode[2]:
                        cx, cy, targetStatus = findCenter(self, c, frame, capture_width, capture_height)
                        targetList.append((cx, cy, area, targetStatus))

            targetList.sort(key=lambda x: int(x[2]))
            targetList.reverse()

            cv2.circle(frame, (int(cw), int(ch)), correctionThreshold, (255, 255, 255), 1)
            cv2.circle(frame, (int(cw), int(ch)), 2, (255, 255, 255), 2)
            
            try: 
                cxMax, cyMax = int(targetList[0][0]), int(targetList[0][1])
                #cv2.circle(frame, (cxMax, cyMax), 10, (0, 0, 255), -1)             #red target
            except: None

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

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream) 

            #cv2.imshow("ROVcontrol Capture", frame)
            #try: return targetList, xAverage, yAverage, frame
            #except: return targetList, 320, 240, frame

        Camera1.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Mask Sliders Setup
        Sliders = Frame(ControlPanel, padx=10, pady=10, background='#c93939', width=400, height=240)

        self.lower_mask = DoubleVar()
        maskLabel = Label(Sliders, text='Lower Mask    -    Upper Mask')
        maskLabel.pack(side=TOP)

        ChannelB = Frame(Sliders, padx=10, pady=10, background='#c93939')
        self.B_lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.B_upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.B_lower_mask_slider.set(self.B_lower_threshold)
        self.B_upper_mask_slider.set(self.B_upper_threshold)
        self.B_lower_mask_slider.pack()
        self.B_upper_mask_slider.pack()
        ChannelB.pack()

        ChannelG = Frame(Sliders, padx=10, pady=10, background='#c93939')
        self.G_lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.G_upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.G_lower_mask_slider.set(self.G_lower_threshold)
        self.G_upper_mask_slider.set(self.G_upper_threshold)
        self.G_lower_mask_slider.pack()
        self.G_upper_mask_slider.pack()
        ChannelG.pack()

        ChannelR = Frame(Sliders, padx=10, pady=10, background='#c93939')
        self.R_lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.R_upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.R_lower_mask_slider.set(self.R_lower_threshold)
        self.R_upper_mask_slider.set(self.R_upper_threshold)
        self.R_lower_mask_slider.pack()
        self.R_upper_mask_slider.pack()
        ChannelR.pack()

        #lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180, command=mask1Update)
        #upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180, command=mask2Update)

        updateButton = Button(Sliders, text="Update Mask", command=lambda: Calibration.saveConfig(self))
        updateButton.pack(side=BOTTOM)

        Sliders.pack(side=BOTTOM)

        video_stream()
        self.window.mainloop()

    #command=lambda: Calibration.saveConfig('blue', 'upper', slider.get())
    def saveConfig(self):
        '''
        def mask1Update(val):
            Calibration.saveConfig(val)
        '''
        
        config = ConfigParser()
        config.read('config.ini')

        lowerB = self.B_lower_mask_slider.get()
        upperB = self.B_upper_mask_slider.get()
        lowerG = self.G_lower_mask_slider.get()
        upperG = self.G_upper_mask_slider.get()
        lowerR = self.R_lower_mask_slider.get()
        upperR = self.R_upper_mask_slider.get()

        config.set('blue', 'lower', str(lowerB))
        config.set('blue', 'upper', str(upperB))

        config.set('green', 'lower', str(lowerG))
        config.set('green', 'upper', str(upperG))
        
        config.set('red', 'lower', str(lowerR))
        config.set('red', 'upper', str(upperR))

        with open('config.ini', 'w') as f:
            config.write(f)

    def getConfig(self):

        config = ConfigParser()
        config.read('config.ini')

        #B
        self.B_lower_threshold = config.get('blue', 'lower')
        self.B_upper_threshold = config.get('blue', 'upper')

        #G
        self.G_lower_threshold = config.get('green', 'lower')
        self.G_upper_threshold = config.get('green', 'upper')

        #R
        self.R_lower_threshold = config.get('red', 'lower')
        self.R_upper_threshold = config.get('red', 'upper')