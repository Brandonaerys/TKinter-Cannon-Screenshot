import tkinter as tk
import PIL.Image, PIL.ImageTk
import cv2 as cv


class App:
    def __init__(self, name, filename):
        self.window = tk.Tk()
        self.window.name = name
        self.frame = cv.imread(filename)
        #
        self.frame = self.frame[::2,::2]
        #
        self.height, self.width, self.channels = self.frame.shape
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
        self.picture = tk.Canvas(self.window, width = self.width, height = self.height, cursor = "crosshair")
        #event bindings here
        self.picture.bind("<ButtonPress-1>", self.PressOne)
        self.picture.bind("<ButtonPress-3>", self.PressThree)
        self.btn_cal=tk.Button(self.window, text="Calculate", width=50, command=self.Calculate)
        self.btn_cal.pack(anchor=tk.CENTER, expand=True)
        self.picture.pack()
        self.picture.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # initiate variables
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


        self.window.mainloop()
    #binding callbacks
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
        # self.DistanceRatio = self.ThreeDistance / self.OneDistance
        # self.OneActual = float(input("actual length for left click"))
        # self.ThreeActual = self.OneActual * self.DistanceRatio
        # print(self.ThreeActual)
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
App("Image", './20190516_110012.jpg')
