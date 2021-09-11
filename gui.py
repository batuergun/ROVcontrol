from tkinter import *
import tkinter
import cv2
from PIL import ImageTk, Image

class GUI:

    def __init__(self):

        self.window = Tk()
        self.window.title('ROVControl')
        self.window.geometry('1280x750')

        top = Frame(self.window, padx=10, pady=10)
        bottom = Frame(self.window, padx=10, pady=10)
        top.pack()
        bottom.pack()

        ControlPanel = Frame(top, padx=10, pady=10, width=400, height=240)
        ControlPanel.pack(side=LEFT, fill=BOTH)

        # Camera 1 Setup
        Camera1 = Frame(top, padx=10, pady=10, bg='#2aaad1', width=800, height=480)

        #self.lmain = Label(Camera1, width = 640, height = 480)
        #self.lmain.pack()

        Camera1.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Camera 2 Setup
        Camera2 = Frame(ControlPanel, padx=10, pady=10, bg='#7e4ccc', width=400, height=240)

        Camera2.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Mask Sliders Setup
        Sliders = Frame(ControlPanel, padx=10, pady=10, background='#c93939', width=400, height=240)

        self.lower_mask = DoubleVar()
        maskLabel = Label(Sliders, text='Lower Mask    -    Upper Mask')
        maskLabel.pack(side=TOP)

        def mask1Update(val):
            file1 = open("mask1Config.txt","r+")
            file1.write(val)
            file1.close()

        def mask2Update(val):
            file2 = open("mask2Config.txt","r+")
            file2.write(val)
            file2.close()

        lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180, command=mask1Update)
        upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180, command=mask2Update)
        lower_mask_slider.pack(side=LEFT)
        upper_mask_slider.pack(side=LEFT)

        slider1 = lower_mask_slider.get()
        slider2 = upper_mask_slider.get()

        updateButton = Button(Sliders, text="Update Mask") #command=lambda: GUI.mask1Update(slider1, slider2)
        updateButton.pack(side=BOTTOM)

        Sliders.pack(fill=BOTH)

        # PWM Monitor Setup
        PWM = Frame(bottom, padx=10, pady=10, background='#4ecc81', width=400, height=240)
        
        topsignals = Frame(PWM, background='#4ecc81', width=400, height=80)
        topsignals.pack(side=TOP, padx= 90)
        leftsignals = Frame(PWM, background='#4ecc81', width=400, height=80)
        leftsignals.pack(side=LEFT)
        rightsignals = Frame(PWM, background='#4ecc81', width=400, height=80)
        rightsignals.pack(side=RIGHT)

        motor5 = Scale(topsignals, from_=1000, to=2000, orient=HORIZONTAL, length= 100, showvalue=0)
        motor6 = Scale(topsignals, from_=1000, to=2000, orient=HORIZONTAL, length= 100, showvalue=0)
        motor5.pack(side=LEFT)
        motor6.pack()

        motor3 = Scale(leftsignals, from_=1000, to=2000, length= 75, showvalue=0)
        motor4 = Scale(leftsignals, from_=1000, to=2000, length= 75, showvalue=0)
        motor3.pack(side=TOP)
        motor4.pack()

        motor1 = Scale(rightsignals, from_=1000, to=2000, length= 75, showvalue=0)
        motor2 = Scale(rightsignals, from_=1000, to=2000, length= 75, showvalue=0)
        motor1.pack(side=TOP)
        motor2.pack()
        
        motor1.set(1500)
        motor2.set(1500)
        motor3.set(1500)
        motor4.set(1500)
        motor5.set(1500)
        motor6.set(1500)

        PWM.pack(side=LEFT)

        # Terminal Setup
        Terminal = Frame(bottom, padx=10, pady=10, background='#777777', width=800, height=240)
        Terminal.pack()

        self.window.mainloop()

    def getMask():
        file1 = open("mask1Config.txt","r+")
        mask1 = file1.read()
        file1.close()

        file2 = open("mask2Config.txt","r+")
        mask2 = file1.read()
        file2.close()

        return mask1, mask2

    def video_stream(self, image):
            #ret, frame = image.read()
            cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
            self.lmain.after(1, GUI.video_stream) 

        