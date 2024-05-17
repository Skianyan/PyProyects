import math
from tkinter import *
import tkinter as tk

import keyboard
import numpy as np

import objGfxLib as gf
from math import floor
from PIL import Image, ImageDraw, ImageTk

width = 501
height = 501

instances = []

camera = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex(0, 0, 0))
##############################################################################################
# Define color constants
BLUE = (10, 10, 255)
RED = (255, 10, 10)
GREEN = (10, 255, 10)
YELLOW = (238, 232, 170)
PURPLE = (186, 85, 211)
CYAN = (0, 255, 255)

##############################################################################################
# Define Pyramid
# Define top Vertex
vTp = gf.Vertex(0, 0.5, 0)

# Define Bottom Vertexes
vAp = gf.Vertex(-0.5, -0.5, -0.5)
vBp = gf.Vertex(0.5, -0.5, -0.5)
vCp = gf.Vertex(0.5, -0.5, 0.5)
vDp = gf.Vertex(-0.5, -0.5, 0.5)

# Add vertexes to list
pyrVertices = []
pyrVertices.append(vTp), pyrVertices.append(vAp), pyrVertices.append(vBp), pyrVertices.append(vCp), pyrVertices.append(
    vDp)

# Define Triangles
pyrTriangles = [(0, 1, 2, RED), (0, 2, 3, RED), (0, 3, 4, RED),
                (0, 3, 1, YELLOW), (1, 3, 4, YELLOW), (1, 2, 4, CYAN)]

pyramid = gf.Model(pyrVertices, pyrTriangles, gf.Vertex(0, 0, 0), math.sqrt(3))

#Define Cube
vertices = [
    gf.Vertex(1, 1, 1),
    gf.Vertex(-1, 1, 1),
    gf.Vertex(-1, -1, 1),
    gf.Vertex(1, -1, 1),
    gf.Vertex(1, 1, -1),
    gf.Vertex(-1, 1, -1),
    gf.Vertex(-1, -1, -1),
    gf.Vertex(1, -1, -1)]

triangles = [
    gf.Triangle([0, 1, 2], RED, [gf.Vertex(0, 0, 1), gf.Vertex(0, 0, 1), gf.Vertex(0, 0, 1)]),
    gf.Triangle([0, 2, 3], RED, [gf.Vertex(0, 0, 1), gf.Vertex(0, 0, 1), gf.Vertex(0, 0, 1)]),
    gf.Triangle([4, 0, 3], GREEN, [gf.Vertex(1, 0, 0), gf.Vertex(1, 0, 0), gf.Vertex(1, 0, 0)]),
    gf.Triangle([4, 3, 7], GREEN, [gf.Vertex(1, 0, 0), gf.Vertex(1, 0, 0), gf.Vertex(1, 0, 0)]),
    gf.Triangle([5, 4, 7], BLUE, [gf.Vertex(0, 0, -1), gf.Vertex(0, 0, -1), gf.Vertex(0, 0, -1)]),
    gf.Triangle([5, 7, 6], BLUE, [gf.Vertex(0, 0, -1), gf.Vertex(0, 0, -1), gf.Vertex(0, 0, -1)]),
    gf.Triangle([1, 5, 6], YELLOW, [gf.Vertex(-1, 0, 0), gf.Vertex(-1, 0, 0), gf.Vertex(-1, 0, 0)]),
    gf.Triangle([1, 6, 2], YELLOW, [gf.Vertex(-1, 0, 0), gf.Vertex(-1, 0, 0), gf.Vertex(-1, 0, 0)]),
    gf.Triangle([1, 0, 5], PURPLE, [gf.Vertex(0, 1, 0), gf.Vertex(0, 1, 0), gf.Vertex(0, 1, 0)]),
    gf.Triangle([5, 0, 4], PURPLE, [gf.Vertex(0, 1, 0), gf.Vertex(0, 1, 0), gf.Vertex(0, 1, 0)]),
    gf.Triangle([2, 6, 7], CYAN, [gf.Vertex(0, -1, 0), gf.Vertex(0, -1, 0), gf.Vertex(0, -1, 0)]),
    gf.Triangle([2, 7, 3], CYAN, [gf.Vertex(0, -1, 0), gf.Vertex(0, -1, 0), gf.Vertex(0, -1, 0)]),
]

# Definir el modelo de un cubo
cube = gf.Model(vertices, triangles, gf.Vertex(0, 0, 0), math.sqrt(3))


##########################################
# Canvas Commands

def clear_canvas_instances():
    canvas.delete('all')
    canvas.create_image(0, 0, anchor=NW, image=cv)
    instances.clear()

def clear_canvas():
    canvas.delete('all')
    canvas.create_image(0, 0, anchor=NW, image=cv)


def rerender(camera):
    for instance in instances:
        instance.apply_camera_transform(camera)
    clear_canvas()
    renderScene(instances, canvas)


def get_values():
    # Translation values
    ttx = translation_x.get()
    tty = translation_y.get()
    ttz = translation_z.get()

    # Rotation Values
    rtx = rot_x.get()
    rty = rot_y.get()
    rtz = rot_z.get()

    # Scale Value
    sca = scale.get()

    # Converting from 360 degrees
    rtx = (rtx * math.pi) / 180
    rty = (rty * math.pi) / 180
    rtz = (rtz * math.pi) / 180

    # Setting default values if null
    ttx = float(ttx) if ttx else .1
    tty = float(tty) if tty else .1
    ttz = float(ttz) if ttz else .1
    sca = float(sca) if sca else 1

    return ttx, tty, ttz, rtx, rty, rtz, sca


def on_enter(event):
    if event.name == 'enter':
        val = get_values()
        ttx, tty, ttz, rtx, rty, rtz, sca = val
        #print(val)
        shape = dropdown_var.get()
        if shape == "Cube":
            dddShape = gf.Instance(cube, gf.Vertex(ttx, tty, ttz), gf.Vertex(rtx, rty, rtz), sca)
            instances.append(dddShape)
            renderInstance(dddShape, canvas)
        elif shape == "Pyramid":
            dddShape = gf.Instance(pyramid, gf.Vertex(ttx, tty, ttz), gf.Vertex(rtx, rty, rtz), sca)
            instances.append(dddShape)
            renderInstance(dddShape, canvas)

def on_arrow_key_pressed(event):
    cam = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex(0, 0, 0))
    if event.name == 'up':
        cam = gf.Camera(gf.Vertex(0, 1, 0), gf.Vertex(0, 0, 0))
        rerender(cam)
    elif event.name == 'down':
        cam = gf.Camera(gf.Vertex(0, -1, 0), gf.Vertex(0, 0, 0))
        rerender(cam)
    elif event.name == 'left':
        cam = gf.Camera(gf.Vertex(-1, 0, 0), gf.Vertex(0, 0, 0))
        rerender(cam)
    elif event.name == 'right':
        cam = gf.Camera(gf.Vertex(1, 0, 0), gf.Vertex(0, 0, 0))
        rerender(cam)
    elif event.name == ',':
        cam = gf.Camera(gf.Vertex(0, 0, -1), gf.Vertex(0, 0, 0))
        rerender(cam)
    elif event.name == '.':
        cam = gf.Camera(gf.Vertex(0, 0, 1), gf.Vertex(0, 0, 0))
        rerender(cam)
    elif event.name == 'j':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex(0, (math.pi/8), 0))
        rerender(cam)
    elif event.name == 'l':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex(0, (-math.pi/8), 0))
        rerender(cam)
    elif event.name == 'i':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex((math.pi/8), 0, 0))
        rerender(cam)
    elif event.name == 'k':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex((-math.pi/8), 0, 0))
        rerender(cam)
    elif event.name == 'u':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex(0, 0, (-math.pi/8)))
        rerender(cam)
    elif event.name == 'o':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.Vertex(0, 0, (math.pi/8)))
        rerender(cam)
    return camera



##########################################
# Instance Functions
def renderInstance(instance, canvas):
    projected = []
    i = 0
    for V in instance.model.vertices:
        Vn = gf.MultiplyMV(instance.transform, V)
        projected.append(gf.projectVertex(Vn, canvas))
    while i < len(instance.model.triangles):
        gf.renderTriangle(instance.model.triangles[i], projected, canvas)
        i += 1


def renderScene(instances, canvas):
    i = 0
    while i < len(instances):
        renderInstance(instances[i], canvas)
        i += 1


##########################################
# Tkinter root

root = tk.Tk()
root.title("3D Shapes Manipulation")

# Create canvas
image = Image.new('RGB', (width, height), (255, 255, 255))
cv = ImageTk.PhotoImage(image)

# Root Frame
# Create a Canvas widget to display the image
canvas = Canvas(root, width=width, height=500)
canvas.create_image(0, 0, anchor=NW, image=cv)
canvas.pack(side=tk.LEFT)

cWidth = canvas.winfo_reqwidth()
cHeight = canvas.winfo_reqheight()
print(cWidth, cHeight)

# Options Frame
frame_options = tk.Frame()

selector_label = tk.Label(master=frame_options, text="Select a Shape to Add", height=2, width=18)
selector_label.pack(side=tk.TOP, pady=2, padx=5)

dropdown_var = tk.StringVar(frame_options)
dropdown_var.set("Cube")
dropdown_menu = tk.OptionMenu(frame_options, dropdown_var, "Cube", "Pyramid")
dropdown_menu.pack(side=tk.BOTTOM, fill=X, pady=5)

# Translation

frame_translation_labels = tk.Frame()
frame_translation = tk.Frame()

rotation_label = tk.Label(frame_translation_labels, text="Translation")
rotation_label.pack(side=TOP, fill=BOTH, pady=5)

translation_label_x = tk.Label(frame_translation_labels, text="x", width=4)
translation_label_x.pack(side=LEFT)
translation_x = tk.Entry(frame_translation, width=5)
translation_x.pack(side=LEFT)

translation_label_y = tk.Label(frame_translation_labels, text="y", width=4)
translation_label_y.pack(side=LEFT)
translation_y = tk.Entry(frame_translation, width=5)
translation_y.pack(side=LEFT)

translation_label_z = tk.Label(frame_translation_labels, text="z", width=4)
translation_label_z.pack(side=LEFT)
translation_z = tk.Entry(frame_translation, width=5)
translation_z.pack(side=LEFT)

# Rotation

frame_rotx = tk.Frame()
rotation_label_x = tk.Label(frame_rotx, text="x")
rotation_label_x.pack(side=LEFT)
rot_x = tk.Scale(frame_rotx, from_=0, to=360, orient=tk.HORIZONTAL)
rot_x.pack(padx=10, pady=5)

frame_roty = tk.Frame()
rotation_label_x = tk.Label(frame_roty, text="y")
rotation_label_x.pack(side=LEFT)
rot_y = tk.Scale(frame_roty, from_=0, to=360, orient=tk.HORIZONTAL)
rot_y.pack(padx=10, pady=5)

frame_rotz = tk.Frame()
rotation_label_x = tk.Label(frame_rotz, text="z")
rotation_label_x.pack(side=LEFT)
rot_z = tk.Scale(frame_rotz, from_=0, to=360, orient=tk.HORIZONTAL)
rot_z.pack(padx=10, pady=5)

# Scale

frame_scale = tk.Frame()
scale_label = tk.Label(frame_scale, text="Scale", width=4)
scale_label.pack(side=TOP, fill=BOTH, pady=5)
scale = tk.Entry(frame_scale, width=5)
scale.pack(side=BOTTOM)

# Lights Frame

frame_lights_labels = tk.Frame()
frame_lights = tk.Frame()

lights_label = tk.Label(frame_lights_labels, text="Light position")
lights_label.pack(side=TOP, fill=BOTH, pady=5)

lights_label_x = tk.Label(frame_lights_labels, text="x", width=4)
lights_label_x.pack(side=LEFT)
lights_x = tk.Entry(frame_translation, width=5)
lights_x.pack(side=LEFT)

lights_label_y = tk.Label(frame_lights_labels, text="y", width=4)
lights_label_y.pack(side=LEFT)
lights_y = tk.Entry(frame_translation, width=5)
lights_y.pack(side=LEFT)

lights_label_z = tk.Label(frame_lights_labels, text="z", width=4)
lights_label_z.pack(side=LEFT)
lights_z = tk.Entry(frame_translation, width=5)
lights_z.pack(side=LEFT)

# Info Frame
frame_info = tk.Frame()
infolabel = tk.Label(root, text="Press 'enter' to generate polygon")
infolabel.pack(side=tk.BOTTOM)

# Clear Frame
frame_clear = tk.Frame()
clear_button = tk.Button(root, text="Clear", borderwidth=1, command=clear_canvas_instances, width=10)
clear_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# # rerender Frame
# frame_rerender = tk.Frame()
# rerender_button = tk.Button(root, text="Rerender", borderwidth=1, command=rerender(camera=), width=10)
# rerender_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Pack Frames
frame_options.pack()
frame_translation_labels.pack()
frame_translation.pack()
frame_rotx.pack()
frame_roty.pack()
frame_rotz.pack()
frame_scale.pack()
frame_clear.pack()
frame_info.pack()

##########################################
depth_buffer = np.zeros(canvas.size[0] * canvas.size[1])

renderScene(instances, canvas)

keyboard.on_press(on_enter)
keyboard.on_press(on_arrow_key_pressed)

root.mainloop()
