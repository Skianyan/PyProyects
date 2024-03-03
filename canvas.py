import tkinter as tk
import keyboard
from tkinter import *
from PIL import Image, ImageTk

class Pt:
    def __init__(self, x, y, h=1):
        self.x = x
        self.y = y
        self.h = h

#Function to track cursor clicks on canvas
def on_click(event):
    x, y = event.x, event.y
    #Place pixel (Placeholder)
    putPixel(x, y)
    #Add click position to points
    points.append(Pt(x, y))
    print("Clicked at:" + " X: " + str(x) + " Y: " + str(y))

def on_enter(event):
    if event.name == 'enter':

        # draws a line last 2 points clicked
        # if points.__len__() > 1:
        #     drawLine(points[-1], points[-2], "#333")

        print("pressed enter")
def putPixel(x, y, color="#000"):
    canvas.create_rectangle(x, y, x + 1, y + 1, fill=color)

def interpolate (i0,f0,i1,f1):
    if i0 == i1:
        return [f0]
    values = []
    a = (f1-f0)/(i1-i0)
    f = f0
    for i in range(i0, i1 + 1):
        values.append(f)
        f = f + a
    return values
def drawLine(p0, p1, color):
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y

    if abs(x1 - x0) > abs(y1 - y0):
        # Es una linea horizontal
        if x0 > x1:
            x0, x1, y0, y1 = x1, x0, y1, y0
        ys = interpolate(x0, y0, x1, y1)
        for x in range(x0, x1):
            putPixel(int(x), int(ys[x-x0]), color)
    else:
        # Es una linea vertical
        if y0 > y1:
            x0, x1, y0, y1 = x1, x0, y1, y0

        xs = interpolate(y0, x0, y1, x1)

        for y in range(y0, y1):
            putPixel(int(xs[y-y0]), int(y), color);


root = tk.Tk()

# Load your image with Pillow
image = Image.new('RGB', (500, 500), (255, 255, 255))
photo = ImageTk.PhotoImage(image)

# Create a Canvas widget to display the image
canvas = Canvas(root, width=500, height=500)
canvas.create_image(0, 0, anchor=NW, image=photo)

canvas.pack()

######
#Parameters
points = []

######

# Bind mouse click event to the canvas
canvas.bind("<Button-1>", on_click)
keyboard.on_press(on_enter)

root.mainloop()