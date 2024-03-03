import math
import tkinter as tk
import keyboard
from tkinter import *
from PIL import Image, ImageTk, ImageColor

class Pt:
    def __init__(self, x, y, h=1):
        self.x = x
        self.y = y
        self.h = h

#####################################################
# Drawing Functions

# Function to track cursor clicks on canvas
def on_click(event):
    x, y = event.x, event.y
    #Place pixel (Placeholder)
    putPixel(x, y)
    #Add click position to points
    points.append(Pt(x, y))
    print("Clicked at:" + " X: " + str(x) + " Y: " + str(y))

def on_enter(event):
    if event.name == 'enter':

        # Draws a line last 2 points clicked
        # if points.__len__() > 1:
        #     drawLine(points[-1], points[-2], "#333")

        # Centroide...
        # cent = calcular_centroide(points)
        # print(cent.x, cent.y )

        #print(points[-3].x)
        #print(points[-2].x)
        #print(points[-1].x)

        # Draws a Triangle between all the points
        #drawPointTriangle(points[-3], points[-2], points[-1], fill)

        # Draws a polygon between all the points
        drawShadedPolygon(points, fill)

        print("enter/ action done")

        #print(ImageColor.getcolor("#800080", "RGB"))

def putPixel(x, y, color="#A020F0"):
    if is_rgb(color):
        color = rgb_to_hex(color[0],color[1],color[2])
    canvas.create_rectangle(x, y, x + 1, y + 1, outline=color)

def drawPointTriangle(p0, p1, p2, fill):
    # Define correctamente los puntos
    if p1.y < p0.y:
        p0, p1 = p1, p0
        #x0, y0, x1, y1 = x1, y1, x0, y1
    if p2.y < p0.y:
        p0, p2 = p2, p0
        #x0, y0, x2, y2 = x2, y2, x0, y0
    if p2.y < p1.y:
        p1, p2 = p2, p1
        #x1, y1, x2, y2 = x2, y2, x1, y1

    # Definir puntos para legibilidad
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y

    # Trazar las lineas del triangulo
    #drawLine(p0, p1, edge, canvas)
    #drawLine(p1, p2, edge, canvas)
    #drawLine(p2, p0, edge, canvas)

    x01 = interpolate(y0, x0, y1, x1)
    x02 = interpolate(y0, x0, y2, x2)
    x12 = interpolate(y1, x1, y2, x2)

    #print('x01 =', x01)
    #print('x02 =', x02)
    #print('x12 =', x12)

    x01.pop(-1)
    x012 = x01 + x12
    # print('x012 =', x012)
    # print(x012.__len__())
    # print(x02.__len__())

    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        xleft = x02
        xright = x012
    else:
        xleft = x012
        xright = x02

    for y in range(y0, y2 + 1):
        a = round(xleft[y - y0])
        b = round(xright[y - y0])
        for x in range(a, b):
            putPixel(x, y, fill)
def drawShadedTriangle(p0, p1, p2, fill):
    # Define correctamente los puntos
    if p1.y < p0.y:
        p0, p1 = p1, p0
    if p2.y < p0.y:
        p0, p2 = p2, p0
    if p2.y < p1.y:
        p1, p2 = p2, p1

    # Definir los valores de sombreado
    h0 = p0.h
    h1 = p1.h
    h2 = p2.h

    # Definir puntos para legibilidad
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y

    x01 = interpolate(y0, x0, y1, x1)
    h01 = interpolate(y0, h0, y1, h1)
    x02 = interpolate(y0, x0, y2, x2)
    h02 = interpolate(y0, h0, y2, h2)
    x12 = interpolate(y1, x1, y2, x2)
    h12 = interpolate(y1, h1, y2, h2)

    #print('x01 =', x01)
    #print('x02 =', x02)
    #print('x12 =', x12)

    # Concatenate Short sides 'x'
    x01.pop(-1)
    x012 = x01 + x12

    # Concatenate short sides 'h'
    h01.pop(-1)
    h012 = h01 + h12

    #print('x012 =', x012)
    #print(x012.__len__())
    #print(x02.__len__())

    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        xleft = x02
        hleft = h02

        xright = x012
        hright = h012
    else:
        xleft = x012
        hleft = h012

        xright = x02
        hright = h02

    for y in range(y0, y2 + 1):
        xl = round(xleft[y - y0])
        xr = round(xright[y - y0])
        h_seg = interpolate(xl, hleft[y - y0], xr, hright[y - y0])

        for x in range(xl, xr):
            shadedColor0 = int(fill[0] * h_seg[x - xl])
            shadedColor1 = int(fill[1] * h_seg[x - xl])
            shadedColor2 = int(fill[2] * h_seg[x - xl])
            shadedColor = (shadedColor0, shadedColor1, shadedColor2)
            putPixel(x, y, shadedColor)
def drawShadedPolygon(points, fill):
    fill = ImageColor.getcolor(fill, "RGB")
    p_cent = calcular_centroide(points)
    #print("centroide (x,y):", p_cent.x, p_cent.y, p_cent.h)
    n = len(points)
    #print("Cuantos puntos:", n)

    for current_point, next_point in zip(points, points[1:]):
        #print("cp", current_point.x, current_point.y, current_point.h)
        drawShadedTriangle(current_point, next_point, p_cent, fill)
        drawLine(current_point, next_point, "#000")

    if next_point == points[n - 1]:
        #print("cp", current_point.x, current_point.y, current_point.h)
        drawShadedTriangle(points[0], next_point, p_cent, fill)
        drawLine(points[0], next_point, "#000")

    points.clear()
    return
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

########################################
#Calculation Functions

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def is_rgb(color):
    if not isinstance(color, tuple):
        return False
    if len(color) != 3:
        return False
    for component in color:
        if not isinstance(component, int):
            return False
        if component < 0 or component > 255:
            return False
    return True
def calcular_centroide(puntos):
    n = len(puntos)

    sum_x = sum(point.x for point in puntos)
    sum_y = sum(point.y for point in puntos)
    sum_h = sum(point.h for point in puntos)

    centroide_x = int(sum_x / n)
    centroide_y = int(sum_y / n)
    centroide_h = sum_h / n
    cent = Pt(centroide_x, centroide_y, centroide_h)
    return cent
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

#########################################
# Tkinter root


root = tk.Tk()

# Create canvas
image = Image.new('RGB', (500, 500), (255, 255, 255))
cv = ImageTk.PhotoImage(image)

# Create a Canvas widget to display the image
canvas = Canvas(root, width=500, height=500)
canvas.create_image(0, 0, anchor=NW, image=cv)

canvas.pack()

##########################################
# Parameters
points = []
edge = "#000"
fill = "#800080"
##########################################

# Bind mouse click event to the canvas
canvas.bind("<Button-1>", on_click)
keyboard.on_press(on_enter)

root.mainloop()
