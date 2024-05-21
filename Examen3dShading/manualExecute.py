from PIL import Image, ImageDraw
import objGfxLib as gf
import math
import numpy as np

# Tamaño de la imagen
width = 501
height = 501

# Definir un lienzo
canvas = Image.new('RGB', (width, height), (255, 255, 255))

vertices = [
    gf.Vertex(1, 1, 1),
    gf.Vertex(-1, 1, 1),
    gf.Vertex(-1, -1, 1),
    gf.Vertex(1, -1, 1),
    gf.Vertex(1, 1, -1),
    gf.Vertex(-1, 1, -1),
    gf.Vertex(-1, -1, -1),
    gf.Vertex(1, -1, -1)]

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

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

# Hacer 3 instancias del cubo
instances = [gf.Instance(cube, gf.Vertex(-1.5, 0, 7), gf.Identity4x4, 0.75),
             gf.Instance(cube, gf.Vertex(1.25, 2.5, 7.5), gf.MakeOYRotationMatrix(195)),
             gf.Instance(cube, gf.Vertex(0, 0, -10), gf.MakeOYRotationMatrix(195))]

# Parámetros de la cámara
camera = gf.Camera(gf.Vertex(-3, 1, 2), gf.MakeOYRotationMatrix(-30))

s2 = math.sqrt(2)
camera.clipping_planes = [
    gf.Plane(gf.Vertex(0, 0, 1), -1),  # Near
    gf.Plane(gf.Vertex(s2, 0, s2), 0),  # Left
    gf.Plane(gf.Vertex(-s2, 0, s2), 0),  # Right
    gf.Plane(gf.Vertex(0, -s2, s2), 0),  # Top
    gf.Plane(gf.Vertex(0, s2, s2), 0),  # Bottom
]

depth_buffer = np.zeros(canvas.size[0] * canvas.size[1])

# A Light.
LT_AMBIENT = 0;
LT_POINT = 1;
LT_DIRECTIONAL = 2;

lights = [gf.Light(LT_AMBIENT, 0.2), gf.Light(LT_DIRECTIONAL, 0.2, gf.Vertex(-1, 0, 1)),
          gf.Light(LT_POINT, 0.6, gf.Vertex(-3, 2, -10))]

gf.RenderScene(camera, instances, depth_buffer, lights, canvas)

canvas.show()
