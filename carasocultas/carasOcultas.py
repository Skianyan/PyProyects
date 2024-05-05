from PIL import Image, ImageDraw
import graflibC as gf
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
    gf.Triangle([0, 1, 2], RED),
    gf.Triangle([0, 2, 3], RED),
    gf.Triangle([4, 0, 3], GREEN),
    gf.Triangle([4, 3, 7], GREEN),
    gf.Triangle([5, 4, 7], BLUE),
    gf.Triangle([5, 7, 6], BLUE),
    gf.Triangle([1, 5, 6], YELLOW),
    gf.Triangle([1, 6, 2], YELLOW),
    gf.Triangle([4, 5, 1], PURPLE),
    gf.Triangle([4, 1, 0], PURPLE),
    gf.Triangle([2, 6, 7], CYAN),
    gf.Triangle([2, 7, 3], CYAN)]

# Definir el modelo de un cubo
cube = gf.Model(vertices, triangles, gf.Vertex(0, 0, 0), math.sqrt(3))

# DODECAEDRO
## Definir variables
r = 4
h1 = r * 0.999998764
h2 = r * 1.61803199
rr = 1.618037984 * r

cos18 = math.cos(math.radians(18))
sin18 = math.sin(math.radians(18))
cos54 = math.cos(math.radians(54))
sin54 = math.sin(math.radians(54))

P0 = gf.Vertex(0, -r, 0)
P5 = gf.Vertex(0, r, h1 + h2)
P1 = gf.Vertex(r * cos18, -r * sin18, 0)
P6 = gf.Vertex(-P1.x, -P1.y, P5.z)
P2 = gf.Vertex(r * cos54, r * sin54, 0)
P7 = gf.Vertex(-P2.x, -P2.y, P5.z)
P3 = gf.Vertex(-P2.x, P2.y, 0)
P8 = gf.Vertex(-P3.x, -P3.y, P5.z)
P4 = gf.Vertex(-P1.x, P1.y, 0)
P9 = gf.Vertex(P1.x, -P1.y, P5.z)
P10 = gf.Vertex(0, -rr, h1)
P11 = gf.Vertex(P0.x, -P10.y, h2)
P12 = gf.Vertex(rr * cos54, -rr * sin54, h2)
P13 = gf.Vertex(-P12.x, -P12.y, h1)
P14 = gf.Vertex(rr * cos18, -rr * sin18, h1)
P15 = gf.Vertex(-P14.x, -P14.y, h2)
P16 = gf.Vertex(P14.x, -P14.y, h2)
P17 = gf.Vertex(-P16.x, -P16.y, h1)
P18 = gf.Vertex(P9.x, -P12.y, h1)
P19 = gf.Vertex(-P18.x, -P18.y, h2)

dvertices = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19]

dtriangles = [
    gf.Triangle([5, 6, 7], RED),
    gf.Triangle([5, 7, 8], RED),
    gf.Triangle([5, 8, 9], RED),
    gf.Triangle([9, 16, 18], GREEN),
    gf.Triangle([9, 18, 11], GREEN),
    gf.Triangle([9, 11, 5], GREEN),
    gf.Triangle([9, 8, 12], BLUE),
    gf.Triangle([9, 12, 14], BLUE),
    gf.Triangle([9, 14, 16], BLUE),
    gf.Triangle([7, 19, 10], YELLOW),
    gf.Triangle([7, 10, 12], YELLOW),
    gf.Triangle([7, 12, 8], YELLOW),
    gf.Triangle([6, 15, 17], PURPLE),
    gf.Triangle([6, 17, 19], PURPLE),
    gf.Triangle([6, 19, 7], PURPLE),
    gf.Triangle([5, 11, 13], CYAN),
    gf.Triangle([5, 13, 15], CYAN),
    gf.Triangle([5, 15, 6], CYAN),
    gf.Triangle([2, 3, 13], RED),
    gf.Triangle([2, 13, 11], RED),
    gf.Triangle([2, 11, 18], RED),
    gf.Triangle([2, 18, 16], GREEN),
    gf.Triangle([2, 16, 14], GREEN),
    gf.Triangle([2, 14, 1], GREEN),
    gf.Triangle([0, 1, 14], BLUE),
    gf.Triangle([0, 14, 12], BLUE),
    gf.Triangle([0, 12, 10], BLUE),
    gf.Triangle([0, 10, 19], YELLOW),
    gf.Triangle([0, 19, 17], YELLOW),
    gf.Triangle([0, 17, 14], YELLOW),
    gf.Triangle([3, 4, 17], PURPLE),
    gf.Triangle([3, 17, 15], PURPLE),
    gf.Triangle([3, 15, 13], PURPLE),
    gf.Triangle([4, 3, 2], CYAN),
    gf.Triangle([4, 2, 1], CYAN),
    gf.Triangle([4, 1, 0], CYAN),
]
# caras = [
#     (P5, P6, P7, P8, P9),
#     (P9, P16, P18, P11, P5),
#     (P9, P8, P12, P14, P16),
#     (P7, P19, P10, P12, P8),
#     (P6, P15, P17, P19, P7),
#     (P5, P11, P13, P15, P6),
#     (P2, P3, P13, P11, P18),
#     (P2, P18, P16, P14, P1),
#     (P0, P1, P14, P12, P10),
#     (P0, P10, P19, P17, P4),
#     (P3, P4, P17, P15, P13),
#     (P4, P3, P2, P1, P0)
# ]

dodecahedron = gf.Model(dvertices, dtriangles, gf.Vertex(0, 0, 0), math.sqrt(3))

# Hacer 3 instancias del cubo
instances = [gf.Instance(dodecahedron, gf.Vertex(6, 0, 20), gf.MakeOYRotationMatrix(200), 0.75)]

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
lights = [
    gf.Light("ambient",0.2),
    gf.Light("point", 0.6, (2, 1, 0)),
    gf.Light("directional", 0.2, (1, 4, 4))]

depth_buffer = np.zeros(canvas.size[0] * canvas.size[1])

gf.RenderScene(camera, instances, depth_buffer, canvas, lights)

canvas.show()
