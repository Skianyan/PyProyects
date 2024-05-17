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


# ----- Sphere model generator -----
def GenerateSphere(divs, color):
    vertices = []
    triangles = []

    delta_angle = 2.0 * math.pi / divs

    # Generate vertices and normals.
    for d in range(0, divs + 1):
        y = (2.0 / divs) * (d - divs / 2)
        radius = math.sqrt(1.0 - y * y)
        for i in range(0, divs):
            vertex = gf.Vertex(radius * math.cos(i * delta_angle), y, radius * math.sin(i * delta_angle))
            vertices.append(vertex)

    # Generate triangles.
    for d in range(0, divs):
        for i in range(0, divs):
            i0 = d * divs + i
            i1 = (d + 1) * divs + (i + 1) % divs
            i2 = divs * d + (i + 1) % divs
            tri0 = [i0, i1, i2]
            tri1 = [i0, i0 + divs, i1]
            triangles.append(gf.Triangle(tri0, color, [vertices[tri0[0]], vertices[tri0[1]], vertices[tri0[2]]]))
            triangles.append(gf.Triangle(tri1, color, [vertices[tri1[0]], vertices[tri1[1]], vertices[tri1[2]]]))

    return gf.Model(vertices, triangles, gf.Vertex(0, 0, 0), 1.0)


sphere = GenerateSphere(25, GREEN)
# instance = gl.Instance(sphere, Vertex(x, y, z), rotation, scale)

# Hacer 3 instancias del cubo
instances = [gf.Instance(sphere, gf.Vertex(-1.5, -1, 6), gf.Identity4x4, 1),
             gf.Instance(cube, gf.Vertex(1.25, 1.5, 6), gf.MakeOYRotationMatrix(195))]

# Parámetros de la cámara
camera = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeOYRotationMatrix(0))

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
