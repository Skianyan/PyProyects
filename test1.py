import math
from PIL import Image, ImageDraw
import graphlibC as gf

# Tamaño de la imagen
width = 1000
height = 1000

# Definir un lienzo
canvas = Image.new('RGB', (width, height), (255, 255, 255))

# Colores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

r = 1  # Radius of the dodecahedron
rr = r * math.sqrt(3)
h1 = r * (1 + math.sqrt(5)) / 2
h2 = r * (3 + math.sqrt(5)) / 2
def deg_to_rad(deg):
    return deg * math.pi / 180

P1 = (0, -r, 0 +.001)
P2 = (r * math.cos(deg_to_rad(18)), -r * math.sin(deg_to_rad(18)), 0 +.001)
P3 = (r * math.cos(deg_to_rad(54)), r * math.sin(deg_to_rad(54)), 0 +.001)
P4 = (-P3[0], P3[1], 0 +.001)
P5 = (-P2[0], P2[1], 0 +.001)
P6 = (0, r, h1 + h2 +.001)
P7 = (-P2[0], -P2[1], P6[2] +.001)
P8 = (-P3[0], -P3[1], P6[2] +.001)
P9 = (-P4[0], -P4[1], P6[2] +.001)
P10 = (P2[0], -P2[1], P6[2] +.001)
P11 = (0, -rr, h1 +.001)
P12 = (P1[0], -P11[1], h2 +.001)
P13 = (rr * math.cos(deg_to_rad(54)), -rr * math.sin(deg_to_rad(54)), h2 +.001)
P14 = (-P13[0], -P13[1], h1 +.001)
P15 = (rr * math.cos(deg_to_rad(18)), -rr * math.sin(deg_to_rad(18)), h1 +.001)
P16 = (-P15[0], -P15[1], h2 +.001)
P17 = (P15[0], -P15[1], h2 +.001)
P18 = (-P17[0], -P17[1], h1 +.001)
P19 = (P10[0], -P13[1], h1 +.001)
P20 = (-P19[0], -P19[1], h2 +.001)

# Define the vertices of a dodecahedron
vertices = [
    gf.Vertex(*P1),
    gf.Vertex(*P2),
    gf.Vertex(*P3),
    gf.Vertex(*P4),
    gf.Vertex(*P5),
    gf.Vertex(*P6),
    gf.Vertex(*P7),
    gf.Vertex(*P8),
    gf.Vertex(*P9),
    gf.Vertex(*P10),
    gf.Vertex(*P11),
    gf.Vertex(*P12),
    gf.Vertex(*P13),
    gf.Vertex(*P14),
    gf.Vertex(*P15),
    gf.Vertex(*P16),
    gf.Vertex(*P17),
    gf.Vertex(*P18),
    gf.Vertex(*P19),
    gf.Vertex(*P20)
]

# Define triangles for the dodecahedron
triangles = [

]


# Render the dodecahedron
gf.renderObject(vertices, triangles, canvas)
canvas.show()
