import cv2 as cv
import numpy as np
import math
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

class VideoCapture:
    def __init__(self, video_source):
        # Open the video source
        self.vid = cv.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # Get video source width and height
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

class Screenshot:
    def __init__(self, frame, Width, Height, parent):
        self.frame = frame
        # cv.imshow("frame", self.frame)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
        self.newTk = tk.Toplevel(parent)
        self.newTk.name = "Screenshot"
        self.picture = tk.Canvas(self.newTk, width = Width, height = Height, cursor = "crosshair")

        self.picture.bind("<ButtonPress-1>", self.PressOne)
        self.picture.bind("<ButtonPress-3>", self.PressThree)
        self.btn_cal=tk.Button(self.newTk, text="Calculate", width=50, command=self.Calculate)
        self.btn_cal.pack(anchor=tk.CENTER, expand=True)
        self.picture.pack()
        self.picture.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.picture.focus_set()

        self.lineOne = self.picture.create_line(0, 0, 1, 1, width = 4, fill = "blue", smooth = 1)
        self.lineThree = self.picture.create_line(0, 0, 1, 1, width = 4, fill = "blue", smooth = 1)
        self.black = self.picture.create_line(0, 0, 1, 1, width = 4, fill = "blue", smooth = 1)
        self.OneX = [-1 for i in range (0, 2)]
        self.OneY = [-1 for i in range (0, 2)]
        self.ThreeX = [-1 for i in range (0, 2)]
        self.ThreeY = [-1 for i in range (0, 2)]
        self.OneCount = 0
        self.ThreeCount = 0
        self.OneDistance = 0
        self.ThreeDistance = 0
        self.DistanceRatio = 0
        self.OneActual = 0
        self.ThreeActual = 0


    def PressOne(self, event):
        self.picture.delete(self.lineOne)
        self.OneX[self.OneCount] = event.x
        self.OneY[self.OneCount] = event.y
        if self.OneCount == 0:
            self.OneCount = 1
        elif self.OneCount == 1:
            self.OneCount = 0
        if not((-1 in self.OneX) or (-1 in self.OneY)):
            self.lineOne = self.picture.create_line(self.OneX[0], self.OneY[0], self.OneX[1], self.OneY[1], width = 4, fill = "blue", smooth = 1)
            self.OneDistance = (((self.OneX[0] - self.OneX[1]) ** 2) + ((self.OneY[0] - self.OneY[1]) ** 2)) ** 0.5
    def PressThree(self, event):
        self.picture.delete(self.lineThree)
        self.ThreeX[self.ThreeCount] = event.x
        self.ThreeY[self.ThreeCount] = event.y
        if self.ThreeCount == 0:
            self.ThreeCount = 1
        elif self.ThreeCount == 1:
            self.ThreeCount = 0
        if not((-1 in self.ThreeX) or (-1 in self.ThreeY)):
            self.lineThree = self.picture.create_line(self.ThreeX[0], self.ThreeY[0], self.ThreeX[1], self.ThreeY[1], width = 4, fill = "green", smooth = 1)
            self.ThreeDistance = (((self.ThreeX[0] - self.ThreeX[1]) ** 2) + ((self.ThreeY[0] - self.ThreeY[1]) ** 2)) ** 0.5

    def Calculate(self):
        self.picture.delete(self.black)
        self.DiameterRatio = self.ThreeDistance / self.OneDistance
        self.OneMidpoint = [(self.OneX[0] + self.OneX[1])/2, (self.OneY[0] + self.OneY[1])/2]
        self.ThreeMidpoint = [(self.ThreeX[0] + self.ThreeX[1])/2, (self.ThreeY[0] + self.ThreeY[1])/2]
        self.black = self.picture.create_line(self.OneMidpoint, self.ThreeMidpoint, width = 4, fill = "black", smooth = 1)
        self.LengthDistance = (((self.ThreeMidpoint[0] - self.OneMidpoint[0]) ** 2) + ((self.ThreeMidpoint[1] - self.OneMidpoint[1]) ** 2)) ** 0.5
        self.OneActual = float(input("actual length for left click: "))
        self.ThreeActual = self.OneActual * self.DiameterRatio
        print("Right Click Diameter", self.ThreeActual)
        self.LengthRatio = self.LengthDistance / self.OneDistance
        self.LengthActual = self.OneActual * self.LengthRatio
        print("Length", self.LengthActual)

class App:
    def __init__(self, window, window_title, video_source):
        # setup tk widget
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = VideoCapture(self.video_source)
        self.canvas = tk.Canvas(self.window, width = self.vid.width, height = self.vid.height)

        self.btn_screenshot=tk.Button(self.window, text="Screenshot", width=50, command=self.screenshot)
        self.btn_screenshot.pack(anchor=tk.CENTER, expand=True)

        self.canvas.pack()
        self.delay = 5
        self.update()

        self.window.mainloop()

    def screenshot(self):
        self.obj = Screenshot(self.orig_frame, self.vid.width, self.vid.height, self.window)

    def update(self):
        ret, self.orig_frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.orig_frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
App(tk.Tk(), "Video Feed", "./2019-06-09 17.10.27.448852.avi")
