import cv2 as cv
import numpy as np
import math
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk


class App:
    def __init__(self, window, window_title, image_path="background.jpg"):
        # set video origin
        self.video = cv.VideoCapture("./Test_RLWBBC_2.mov")
        print("press 's' for screenshots")
        time.sleep(1)
        # setup tk widget
        self.window = window
        self.window.title(window_title)
        # play video stream
        while True:
            self.ret, self.orig_frame = self.video.read()
            self.height, self.width = self.orig_frame.shape[:2]

            cv.imshow("frame", self.orig_frame)

            self.key = cv.waitKey(1)
            if self.key & 0xFF == ord('q'):
                break
            elif self.key & 0xFF == ord('s'):
                self.img =  cv.cvtColor(self.orig_frame, cv.COLOR_BGR2RGB)
                break
        self.video.release()
        # create canvas that fits the screenshot
        self.canvas = tk.Canvas(self.window, width = self.width, height = self.height)
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.img))
        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        # bind canvas events
        self.canvas.bind("<ButtonPress-1>", self.Press)
        self.canvas.bind("<ButtonRelease-1>", self.Release)
        self.canvas.bind("<Return>", self.LengthCalculator)
        self.canvas.pack()
        self.window.mainloop()
        self.Press = [[-1,-1], [-1,-1]]
        self.Release = [[-1,-1], [-1,-1]]
        self.PressCount = 0
        print(self.PressCount)
        self.ReleaseCount = 0
        # Callback for the "Blur" button

    def Press(self, event):
        self.canvas.focus_set()
        self.Press[self.PressCount][0] = event.x
        self.Press[self.PressCount][1] = event.y
        self.PressCount += 1
    def Release(self, event):
        self.canvas.focus_set()
        self.Release[self.ReleaseCount][0] = event.x
        self.Release[self.ReleaseCount][1] = event.y
        self.ReleaseCount += 1
        self.canvas.create_line(self.Press[self.ReleaseCount][0], self.Press[self.ReleaseCount][1], self.Release[self.ReleaseCount][0], self.Release[self.ReleaseCount][1])

    def LengthCalculator():
        self.MidOne = [(self.Press[0][0] + self.Release[0][0]) / 2, (self.Press[0][1] + self.Release[0][1]) / 2]
        self.MidTwo = [(self.Press[1][0] + self.Release[1][0]) / 2, (self.Press[1][1] + self.Release[1][1]) / 2]
        self.hypo = math.sqrt((self.MidOne[0] - self.MidTwo[0]) ** 2 + (self.MidOne[1] - self.MidTwo[1]) ** 2)
        print(self.hypo)
# Create a window and pass it to the Application object
Obj = App(tk.Tk(), "Screenshot")
