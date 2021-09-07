from tkinter import *
import tkinter
import cv2
from PIL import ImageTk, Image

class GUI:

    def __init__(self, capture):
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

        self.vid = VideoCapture(capture)
        self.canvas = Canvas(Camera1, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        Camera1.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Camera 2 Setup
        Camera2 = Frame(ControlPanel, padx=10, pady=10, bg='#7e4ccc', width=400, height=240)

        Camera2.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Mask Sliders Setup
        Sliders = Frame(ControlPanel, padx=10, pady=10, background='#c93939', width=400, height=240)

        lower_mask = DoubleVar()
        maskLabel = Label(Sliders, text='Lower Mask    -    Upper Mask')
        maskLabel.pack(side=TOP)
        lower_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        upper_mask_slider = Scale(Sliders, from_=0, to=255, orient=HORIZONTAL, length= 180)
        lower_mask_slider.pack(side=LEFT)
        upper_mask_slider.pack(side=LEFT)

        updateButton = Button(Sliders, text="Update Mask", command=lambda: self.maskUpdate(lower_mask_slider.get()))
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

        self.delay = 15
        self.update()

        self.window.mainloop()

        return lower_mask_slider.get()

    def maskUpdate(self, maskValue):
        return str(maskValue)

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
        self.window.after(self.delay, self.update)

class VideoCapture:

    def __init__(self, capture):
        self.vid = capture
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source")
 
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)