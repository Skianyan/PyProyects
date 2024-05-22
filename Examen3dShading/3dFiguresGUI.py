import math
from tkinter import *
import tkinter as tk

import keyboard
import numpy as np

import objGfxLib as gf
from math import floor
from PIL import Image, ImageDraw, ImageTk

width = 551
height = 551

instances = []

global camera
camera = gf.Camera(gf.Vertex(0, 0, 0), gf.Identity4x4)

s2 = math.sqrt(2)
camera.clipping_planes = [
    gf.Plane(gf.Vertex(0, 0, 1), -1),  # Near
    gf.Plane(gf.Vertex(s2, 0, s2), 0),  # Left
    gf.Plane(gf.Vertex(-s2, 0, s2), 0),  # Right
    gf.Plane(gf.Vertex(0, -s2, s2), 0),  # Top
    gf.Plane(gf.Vertex(0, s2, s2), 0),  # Bottom
]

# A Light.
LT_AMBIENT = 0;
LT_POINT = 1;
LT_DIRECTIONAL = 2;

lights = [gf.Light(LT_AMBIENT, 0.2), gf.Light(LT_DIRECTIONAL, 0.2, gf.Vertex(-1, 0, 1)),
          gf.Light(LT_POINT, 0.6, gf.Vertex(0, 0, 0))]

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
# Definir el vértice superior
vTp = gf.Vertex(0, 0.5, 0)

# Definir los vértices inferiores
vAp = gf.Vertex(-0.5, -0.5, -0.5)
vBp = gf.Vertex(0.5, -0.5, -0.5)
vCp = gf.Vertex(0.5, -0.5, 0.5)
vDp = gf.Vertex(-0.5, -0.5, 0.5)

# Agregar vértices a la lista
pyrVertices = [vTp, vAp, vBp, vCp, vDp]

# Definir triángulos
pyrTriangles = [
    (0, 1, 2, RED),
    (0, 2, 3, RED),
    (0, 3, 4, RED),
    (0, 4, 1, YELLOW),
    (1, 3, 4, YELLOW),
    (1, 2, 3, CYAN)
]

normals = [
    gf.calculate_normal(pyrVertices[0], pyrVertices[1], pyrVertices[2]),
    gf.calculate_normal(pyrVertices[0], pyrVertices[2], pyrVertices[3]),
    gf.calculate_normal(pyrVertices[0], pyrVertices[3], pyrVertices[4]),
    gf.calculate_normal(pyrVertices[0], pyrVertices[4], pyrVertices[1]),
    gf.calculate_normal(pyrVertices[1], pyrVertices[2], pyrVertices[3]),
    gf.calculate_normal(pyrVertices[1], pyrVertices[3], pyrVertices[4])
]

# Crear los triángulos con sus normales y colores
pyrTrianglesWithNormals = [
    gf.Triangle([0, 1, 2], RED, [normals[0], normals[0], normals[0]]),
    gf.Triangle([0, 2, 3], RED, [normals[1], normals[1], normals[1]]),
    gf.Triangle([0, 3, 4], RED, [normals[2], normals[2], normals[2]]),
    gf.Triangle([0, 4, 1], YELLOW, [normals[3], normals[3], normals[3]]),
    gf.Triangle([1, 2, 3], YELLOW, [normals[4], normals[4], normals[4]]),
    gf.Triangle([1, 3, 4], CYAN, [normals[5], normals[5], normals[5]])
]

# Definir el modelo de la pirámide
pyramid = gf.Model(pyrVertices, pyrTrianglesWithNormals, gf.Vertex(0, 0, 0), math.sqrt(3))

# Define Cube
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

sphere = gf.GenerateSphere(25, GREEN)


# instance = gl.Instance(sphere, Vertex(x, y, z), rotation, scale)


##########################################
# Canvas Commands

def clear_canvas_instances():
    canvas.delete('all')
    canvas.create_image(0, 0, anchor=NW, image=cv)
    instances.clear()


def clear_canvas():
    canvas.delete('all')
    canvas.create_image(0, 0, anchor=NW, image=cv)


def rerender(newcam):
    global depth_buffer
    depth_buffer = np.zeros(image.size[0] * image.size[1])
    for instance in instances:
        instance.apply_camera_transform(newcam)
    clear_canvas()
    gf.RenderScene(camera, instances, depth_buffer, lights, canvas)


def relight():
    lx, ly, lz = getlight()
    global depth_buffer
    depth_buffer = np.zeros(image.size[0] * image.size[1])
    clear_canvas()
    newlight = [gf.Light(LT_AMBIENT, 0.2), gf.Light(LT_DIRECTIONAL, 0.2, gf.Vertex(-1, 0, 1)),
                gf.Light(LT_POINT, 0.6, gf.Vertex(lx, ly, lz))]
    gf.RenderScene(camera, instances, depth_buffer, newlight, canvas)


def getlight():
    lx = light_x.get()
    ly = light_y.get()
    lz = light_z.get()
    lx = float(lx) if lx else 0
    ly = float(ly) if ly else 0
    lz = float(lz) if lz else 0
    return lx, ly, lz


def get_values():
    ttx = translation_x.get()
    tty = translation_y.get()
    ttz = translation_z.get()
    rtx = rot_x.get()
    rty = rot_y.get()
    rtz = rot_z.get()

    sca = scale.get()

    rtx = (rtx * math.pi) / 180
    rty = (rty * math.pi) / 180
    rtz = (rtz * math.pi) / 180

    ttx = float(ttx) if ttx else 0
    tty = float(tty) if tty else 0
    ttz = float(ttz) if ttz else 0
    sca = float(sca) if sca else 1

    return ttx, tty, ttz, rtx, rty, rtz, sca


def on_enter(event):
    if event.name == 'enter':
        val = get_values()
        ttx, tty, ttz, rtx, rty, rtz, sca = val
        shape = selector_var.get()
        rendtype = render_var.get()
        if shape == "Cube":
            dddShape = gf.Instance(cube, gf.Vertex(ttx, tty, ttz), gf.MakeRotationMatrix(gf.Vertex(rtx, rty, rtz)),
                                   sca, rendtype)
            instances.append(dddShape)
            gf.RenderScene(camera, instances, depth_buffer, lights, canvas)
        elif shape == "Pyramid":
            dddShape = gf.Instance(pyramid, gf.Vertex(ttx, tty, ttz), gf.MakeRotationMatrix(gf.Vertex(rtx, rty, rtz)),
                                   sca, rendtype)
            instances.append(dddShape)
            gf.RenderScene(camera, instances, depth_buffer, lights, canvas)
        elif shape == "Sphere":
            dddShape = gf.Instance(sphere, gf.Vertex(ttx, tty, ttz), gf.MakeRotationMatrix(gf.Vertex(rtx, rty, rtz)),
                                   sca, rendtype)
            instances.append(dddShape)
            gf.RenderScene(camera, instances, depth_buffer, lights, canvas)


def on_test(event):
    if event.name == 'z':
        global depth_buffer
        global camera
        # Debugging
        print("---------------")
        print("Camera pos: " + str(camera.position.x), str(camera.position.y), str(camera.position.z))
        print("Camera ori: " + str(camera.orientation.data))
        print("Instances: " + str(len(instances)))
        for i in range(len(instances)):
            print("Instance " + str(i + 1) + " pos: " + str(instances[i].position.x), str(instances[i].position.y),
                  str(instances[i].position.z))
            print("Instance " + str(i + 1) + " ori: " + str(instances[i].orientation.data))
        print("Depth Buffer: " + str(depth_buffer))
        print("Lights: " + str(lights[0].tipo), str(lights[1].direction.x), str(lights[2].intensity))
        print("---------------")
    if event.name == 'x':
        print("added cube")
        depth_buffer = np.zeros(image.size[0] * image.size[1])
        shape = gf.Instance(cube, gf.Vertex(0, 0, 30), gf.Identity4x4, 1, "Flat")
        instances.append(shape)
        gf.RenderScene(camera, instances, depth_buffer, lights, canvas)
    if event.name == 'f':
        print("Reload")
        clear_canvas()
        depth_buffer = np.zeros(image.size[0] * image.size[1])
        gf.RenderScene(camera, instances, depth_buffer, lights, canvas)
    if event.name == 'g':
        print("Reload Lights")
        relight()
    if event.name == 'c':
        print("cleared all instances")
        print(gf.MakeRotationMatrix(gf.Vertex(0, (math.pi / 8), 0)).data)
        clear_canvas_instances()


def on_arrow_key_pressed(event):
    if event.name == 'w':
        cam = gf.Camera(gf.Vertex(0, 1, 0), gf.Identity4x4)
        rerender(cam)
    elif event.name == 's':
        cam = gf.Camera(gf.Vertex(0, -1, 0), gf.Identity4x4)
        rerender(cam)
    elif event.name == 'a':
        cam = gf.Camera(gf.Vertex(-1, 0, 0), gf.Identity4x4)
        rerender(cam)
    elif event.name == 'd':
        cam = gf.Camera(gf.Vertex(1, 0, 0), gf.Identity4x4)
        rerender(cam)
    elif event.name == ',':
        cam = gf.Camera(gf.Vertex(0, 0, -5), gf.Identity4x4)
        rerender(cam)
    elif event.name == '.':
        cam = gf.Camera(gf.Vertex(0, 0, 5), gf.Identity4x4)
        rerender(cam)
    elif event.name == 'j':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeRotationMatrix(gf.Vertex(0, (math.pi / 8), 0)))
        rerender(cam)
    elif event.name == 'l':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeRotationMatrix(gf.Vertex(0, (-math.pi / 8), 0)))
        rerender(cam)
    elif event.name == 'i':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeRotationMatrix(gf.Vertex((math.pi / 8), 0, 0)))
        rerender(cam)
    elif event.name == 'k':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeRotationMatrix(gf.Vertex((-math.pi / 8), 0, 0)))
        rerender(cam)
    elif event.name == 'u':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeRotationMatrix(gf.Vertex(0, 0, (-math.pi / 8))))
        rerender(cam)
    elif event.name == 'o':
        cam = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeRotationMatrix(gf.Vertex(0, 0, (math.pi / 8))))
        rerender(cam)


##########################################
# Tkinter root

root = tk.Tk()
root.title("3D Shapes Manipulation")

# Create canvas
image = Image.new('RGB', (width, height), (255, 255, 255))
cv = ImageTk.PhotoImage(image)

# Root Frame
# Create a Canvas widget to display the image
canvas = Canvas(root, width=550, height=550)
canvas.create_image(0, 0, anchor=NW, image=cv)
canvas.pack(side=tk.LEFT)

cWidth = canvas.winfo_reqwidth()
cHeight = canvas.winfo_reqheight()

# print("Canvas dimensions")
# print(cWidth, cHeight)

# Options Frame
frame_options = tk.Frame()

# Shape Selector
selector_label = tk.Label(master=frame_options, text="Select a Shape to Add", height=2, width=18)
selector_label.pack(side=tk.TOP, pady=2, padx=5)

selector_var = tk.StringVar(frame_options)
selector_var.set("Cube")
selector_menu = tk.OptionMenu(frame_options, selector_var, "Cube", "Pyramid", "Sphere")
selector_menu.pack(side=tk.BOTTOM, fill=X, pady=5)

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

# Lights

frame_light_labels = tk.Frame()
frame_light = tk.Frame()

rotation_label = tk.Label(frame_light_labels, text="Light source")
rotation_label.pack(side=TOP, fill=BOTH, pady=5)

light_label_x = tk.Label(frame_light_labels, text="x", width=4)
light_label_x.pack(side=LEFT)
light_x = tk.Entry(frame_light, width=5)
light_x.pack(side=LEFT)

light_label_y = tk.Label(frame_light_labels, text="y", width=4)
light_label_y.pack(side=LEFT)
light_y = tk.Entry(frame_light, width=5)
light_y.pack(side=LEFT)

light_label_z = tk.Label(frame_light_labels, text="z", width=4)
light_label_z.pack(side=LEFT)
light_z = tk.Entry(frame_light, width=5)
light_z.pack(side=LEFT)

# Rendering Selector
render_options = tk.Frame()

render_label = tk.Label(master=render_options, text="Select a Render Method", height=2, width=18)
render_label.pack(side=tk.TOP, pady=2, padx=5)

render_var = tk.StringVar(frame_options)
render_var.set("Phong")
render_menu = tk.OptionMenu(render_options, render_var, "Phong", "Gouraud", "Flat")
render_menu.pack(side=tk.BOTTOM, fill=X, pady=5)

# Info Frame
frame_info = tk.Frame()
infolabel = tk.Label(root, text="Press 'enter' to generate polygon")
infolabel.pack(side=tk.BOTTOM)

# Clear Frame
frame_clear = tk.Frame()
clear_button = tk.Button(root, text="Clear", borderwidth=1, command=clear_canvas_instances, width=10)
clear_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Pack Frames
frame_options.pack()
render_options.pack()
frame_translation_labels.pack()
frame_translation.pack()
frame_rotx.pack()
frame_roty.pack()
frame_rotz.pack()
frame_scale.pack()
frame_light_labels.pack()
frame_light.pack()
frame_clear.pack()
frame_info.pack()

depth_buffer = np.zeros(image.size[0] * image.size[1])

gf.RenderScene(camera, instances, depth_buffer, lights, image)

keyboard.on_press(on_enter)
keyboard.on_press(on_test)
keyboard.on_press(on_arrow_key_pressed)

root.mainloop()
