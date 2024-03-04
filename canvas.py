import math
import tkinter as tk
import keyboard
from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk, ImageColor


class Pt:
    def __init__(self, x, y, h=1):
        self.x = x
        self.y = y
        self.h = h

##########################################
# Drawing Functions


def putPixel(x, y, color):
    if is_rgb(color):
        color = rgb_to_hex(color[0],color[1],color[2])
    canvas.create_rectangle(x, y, x + 1, y + 1, outline=color)


def drawShadedTriangle(p0, p1, p2, fill):
    if is_rgb(fill) == FALSE:
        fill = ImageColor.getcolor(fill, "RGB")

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
        #drawLine(current_point, next_point, "#000")

    if next_point == points[n - 1]:
        #print("cp", current_point.x, current_point.y, current_point.h)
        drawShadedTriangle(points[0], next_point, p_cent, fill)
        #drawLine(points[0], next_point, "#000")

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

##########################################
# Calculation Functions


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


def getIntValue(value, min, max):
    try:
        value = int(input("Define " + value + ": "))
    except ValueError:
        print('Enter a valid integer')
    if value > max:
        print("Please enter a number smaller than " + str(max))
    if value < min:
        print("Please enter a number larger than " + str(min))

        exit()
    return value


##########################################
# UI Functions
# Function to track cursor clicks on canvas


def on_click(event):
    if points.__len__() < 7:
        x, y = event.x, event.y
        #Place pixel (Placeholder)
        putPixel(x, y, color)
        #Add click position to points
        points.append(Pt(x, y))
        print("Clicked at:" + " X: " + str(x) + " Y: " + str(y))
        generate_slider()
    else:
        print("max 7 points")


def on_enter(event):
    if event.name == 'enter' and color is not None:
        sliderval = get_slider_values()
        print("sliderval 'premod'", sliderval)
        sliderval = [x/100 for x in sliderval]
        print("sliderval", sliderval)
        update_h_values(points, sliderval)
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
        # testpuntos =[Pt(100, 100, 1), Pt(100, 200, .9), Pt(200, 200, .6), Pt(200, 100, .4)]
        print(points.__len__())
        if points.__len__() == 2:
            drawLine(points[-2], points[-1], color)
            reset_params()
        if points.__len__() == 3:
            drawShadedTriangle(points[-3], points[-2], points[-1], color)
            reset_params()
        if points.__len__() > 3:
            drawShadedPolygon(points, color)
            reset_params()
        print("enter / action done")
        #print(ImageColor.getcolor("#800080", "RGB"))
    else:
        if event.name == 'enter' and color is not None:
            print("please select a color")


def clear_canvas():
    canvas.delete('all')
    canvas.create_image(0, 0, anchor=NW, image=cv)
    points.clear()
    delete_sliders(frame_sliders)

def generate_slider():
    new_slider = tk.Scale(frame_sliders, from_=0, to=100, orient=tk.HORIZONTAL)
    new_slider.pack(padx=10, pady=5)
    sliders.append(new_slider)

def delete_sliders(frame_sliders):
    for slider in sliders:
        slider.destroy()
    sliders.clear()

def select_color():
    global color
    color = show_color_palette()
    if color:
        color_label.config(bg=color)
    print(color)

def reset_params():
    points.clear()
    delete_sliders(frame_sliders)
    sliders = []
def show_color_palette():
    color = colorchooser.askcolor()[1]
    return color

def update_h_values(points_array, sliders):
    for point, slider_value in zip(points_array, sliders):
        point.h = slider_value
def get_slider_values():
    slider_values = []
    for i, slider in enumerate(sliders):
        value = slider.get()
        print(f"Slider {i + 1} value:", value)
        slider_values.append(value)
    return slider_values

##########################################
# Get Canvas Size > 500

# print("1.- Define canvas size.")
#
# # Get Canvas Width
# width = getIntValue("width", 49, 501)
#
# # Get Canvas Height
# height = getIntValue("height", 49, 501)

# set width for testing

##########################################
# Parameters
points = []
sliders = []
edge = "#000"
funnycolor = ''
color = None
width = 500
height = 500

##########################################
# Tkinter root


root = tk.Tk()
root.title("Shaded Polygon Generator")

# Create canvas
image = Image.new('RGB', (width, height), (255, 255, 255))
cv = ImageTk.PhotoImage(image)

# Root Frame
# Create a Canvas widget to display the image
canvas = Canvas(root, width=width, height=500)
canvas.create_image(0, 0, anchor=NW, image=cv)
canvas.pack(side=tk.LEFT)



# Options Frame
frame_options = tk.Frame()
show_palette_button = tk.Button(master=frame_options, text="Show Palette", command=select_color)
show_palette_button.pack(side=tk.RIGHT, pady=10, padx=5)

color_label = tk.Label(master=frame_options, text="Selected Color", bg="white", height=2, width=15)
color_label.pack(side=tk.LEFT, pady=3, padx=5)

frame_sliders = tk.Frame()

# Info Frame
frame_info = tk.Frame()
infolabel = tk.Label(root, text="Press 'enter' to generate polygon")
infolabel.pack(side=tk.BOTTOM)

# Clear Frame
frame_clear = tk.Frame()
clear_button = tk.Button(root, text="Clear", borderwidth=1, command=clear_canvas, width= 10)
clear_button.pack(side=tk.BOTTOM, padx=5, pady= 5)

# Pack Frames
frame_options.pack()
frame_sliders.pack()
frame_clear.pack()
frame_info.pack()


# Bind mouse click event to the canvas
canvas.bind("<Button-1>", on_click)
keyboard.on_press(on_enter)


root.mainloop()
