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


        # Callback for button
    def screenshot(self):
        ret, orig_frame = self.vid.get_frame()
        self.newTk = tk.Tk()
        self.picture = tk.Canvas(self.newTk, width = self.vid.width, height = self.vid.height)
        self.picture.pack()
        frame = cv.cvtColor(orig_frame, cv.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.picture.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # bind canvas events
        self.picture.bind("<ButtonPress-1>", self.Press)
        self.picture.bind("<ButtonRelease-1>", self.Release)
        self.picture.bind("<Return>", self.LengthCalculator)
        self.picture.pack()
        self.picture.focus_set()
        self.newTk.mainloop()

        self.Press = [[-1,-1], [-1,-1]]
        self.Release = [[-1,-1], [-1,-1]]
        self.PressCount = 0
        self.ReleaseCount = 0

    def update(self):
        ret, orig_frame = self.vid.get_frame()
        if ret:
            frame = cv.cvtColor(orig_frame, cv.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        self.window.after(self.delay, self.update)

    def Press(self, event):
        self.picture.focus_set()
        self.Press[self.PressCount][0] = event.x
        self.Press[self.PressCount][1] = event.y
        self.PressCount += 1
    def Release(self, event):
        self.picture.focus_set()
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
App(tk.Tk(), "Screenshot", "./Test_RLWBBC_1.MOV")
