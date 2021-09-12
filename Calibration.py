from tkinter import *
import tkinter
import cv2
from PIL import ImageTk, Image
from configparser import ConfigParser
import numpy as np
import imutils

class Calibration:

    def __init__(self):

        capture_width, capture_height = 1280, 720
        correctionThreshold = 50
        
        # Limit mode 0 -> [0, areaMinThreshold, None]
        # Limit mode 1 -> [1, areaMinThreshold, areaMaxThreshold]

        Calibration.getConfig(self)
        lower_threshold = np.array([int(self.B_lower), int(self.G_lower), int(self.R_lower)])
        upper_threshold = np.array([int(self.B_upper), int(self.G_upper), int(self.R_upper)])
        limitMode = [int(self.areaMode), int(self.areaMin), int(self.areaMax)]
        
        self.window = Tk()
        self.window.title('ROVControl')
        self.window.geometry('1280x750')

        top = Frame(self.window, padx=10, pady=10)
        top.pack()

        ControlPanel = Frame(top, padx=10, pady=10, width=400, height=240)
        ControlPanel.pack(side=LEFT)

        # Camera 1 Setup
        Camera1 = Frame(top, padx=10, pady=10, width=800, height=480)

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
            Calibration.getConfig(self)
            lower_threshold = np.array([int(self.B_lower), int(self.G_lower), int(self.R_lower)])
            upper_threshold = np.array([int(self.B_upper), int(self.G_upper), int(self.R_upper)])
            limitMode = [int(self.areaMode), int(self.areaMin), int(self.areaMax)]

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
        Sliders = Frame(ControlPanel, padx=10, pady=10, background='#4ecc81', width=400, height=240)

        ChannelB = Frame(Sliders, padx=10, pady=10, background='#4ecc81')
        blueLabel = Label(Sliders, text='Blue', background='#4ecc81')
        self.B_lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.B_upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.B_lower_mask_slider.set(self.B_lower)
        self.B_upper_mask_slider.set(self.B_upper)
        blueLabel.pack()
        self.B_lower_mask_slider.pack()
        self.B_upper_mask_slider.pack()
        ChannelB.pack()

        ChannelG = Frame(Sliders, padx=10, pady=10, background='#4ecc81')
        greenLabel = Label(Sliders, text='Green', background='#4ecc81')
        self.G_lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.G_upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.G_lower_mask_slider.set(self.G_lower)
        self.G_upper_mask_slider.set(self.G_upper)
        greenLabel.pack()
        self.G_lower_mask_slider.pack()
        self.G_upper_mask_slider.pack()
        ChannelG.pack()

        ChannelR = Frame(Sliders, padx=10, pady=10, background='#4ecc81')
        redLabel = Label(Sliders, text='Red', background='#4ecc81')
        self.R_lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.R_upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        self.R_lower_mask_slider.set(self.R_lower)
        self.R_upper_mask_slider.set(self.R_upper)
        redLabel.pack()
        self.R_lower_mask_slider.pack()
        self.R_upper_mask_slider.pack()
        ChannelR.pack()

        ChannelArea = Frame(Sliders, padx=10, pady=10, background='#4ecc81')
        areaLabel = Label(Sliders, text='Area Limit', background='#4ecc81')
        self.mode_area = Scale(Sliders, from_=0, to=1, orient=HORIZONTAL, length= 180)
        self.min_area = Scale(Sliders, from_=0, to=50000, orient=HORIZONTAL, length= 180)
        self.max_area = Scale(Sliders, from_=0, to=50000, orient=HORIZONTAL, length= 180)
        self.mode_area.set(self.areaMode)
        self.min_area.set(self.areaMin)
        self.max_area.set(self.areaMax)
        areaLabel.pack()
        self.mode_area.pack()
        self.min_area.pack()
        self.max_area.pack()
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

        modeArea = self.mode_area.get()
        minArea = self.min_area.get()
        maxArea = self.max_area.get()

        config.set('blue', 'lower', str(lowerB))
        config.set('blue', 'upper', str(upperB))

        config.set('green', 'lower', str(lowerG))
        config.set('green', 'upper', str(upperG))
        
        config.set('red', 'lower', str(lowerR))
        config.set('red', 'upper', str(upperR))

        config.set('area', 'mode', str(modeArea))
        config.set('area', 'min', str(minArea))
        config.set('area', 'max', str(maxArea))

        with open('config.ini', 'w') as f:
            config.write(f)

    def getConfig(self):

        config = ConfigParser()
        config.read('config.ini')

        #B
        self.B_lower = config.get('blue', 'lower')
        self.B_upper = config.get('blue', 'upper')

        #G
        self.G_lower = config.get('green', 'lower')
        self.G_upper = config.get('green', 'upper')

        #R
        self.R_lower = config.get('red', 'lower')
        self.R_upper = config.get('red', 'upper')

        #Area
        self.areaMode = config.get('area', 'mode')
        self.areaMin = config.get('area', 'min')
        self.areaMax = config.get('area', 'max')
