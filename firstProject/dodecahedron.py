import gfxlib as gf
import numpy as np
import math
from PIL import Image, ImageDraw

width = 1000
height = 1000

##############################################################################################

# Definir un lienzo
canvas = Image.new('RGB', (int(width), int(height)), (255, 255, 255))

# Definir Variables

r = 4
h1 = r * 0.999998764
h2 = r * 1.61803199
rr = 1.618037984 * r

cos18 = math.cos(math.radians(18))
sin18 = math.sin(math.radians(18))
cos54 = math.cos(math.radians(54))
sin54 = math.sin(math.radians(54))

# Definir los colores
BLUE = (10, 10, 255)
RED = (255, 10, 10)
GREEN = (10, 255, 10)
YELLOW = (238, 232, 170)
PURPLE = (186, 85, 211)
CYAN = (0, 255, 255)

zoffset = 20

# Definir Vertices
P1 = gf.Vertex(0, -r, 0 + zoffset)
P6 = gf.Vertex(0, r, h1 + h2 + zoffset)
P2 = gf.Vertex(r * cos18, -r * sin18, 0 + zoffset)
P7 = gf.Vertex(-P2.x, -P2.y, P6.z + zoffset)
P3 = gf.Vertex(r * cos54, r * sin54, 0 + zoffset)
P8 = gf.Vertex(-P3.x, -P3.y, P6.z + zoffset)
P4 = gf.Vertex(-P3.x, P3.y, 0 + zoffset)
P9 = gf.Vertex(-P4.x, -P4.y, P6.z + zoffset)
P5 = gf.Vertex(-P2.x, P2.y, 0 + zoffset)
P10 = gf.Vertex(P2.x, -P2.y, P6.z + zoffset)
P11 = gf.Vertex(0, -rr, h1 + zoffset)
P12 = gf.Vertex(P1.x, -P11.y, h2 + zoffset)
P13 = gf.Vertex(rr * cos54, -rr * sin54, h2 + zoffset)
P14 = gf.Vertex(-P13.x, -P13.y, h1 + zoffset)
P15 = gf.Vertex(rr * cos18, -rr * sin18, h1 + zoffset)
P16 = gf.Vertex(-P15.x, -P15.y, h2 + zoffset)
P17 = gf.Vertex(P15.x, -P15.y, h2 + zoffset)
P18 = gf.Vertex(-P17.x, -P17.y, h1 + zoffset)
P19 = gf.Vertex(P10.x, -P13.y, h1 + zoffset)
P20 = gf.Vertex(-P19.x, -P19.y, h2 + zoffset)

# Definir Caras
caras = [
    (P6, P7, P8, P9, P10),
    (P10, P17, P19, P12, P6),
    (P10, P9, P13, P15, P17),
    (P8, P20, P11, P13, P9),
    (P7, P16, P18, P20, P8),
    (P6, P12, P14, P16, P7),
    (P3, P4, P14, P12, P19),
    (P3, P19, P17, P15, P2),
    (P1, P2, P15, P13, P11),
    (P1, P11, P20, P18, P5),
    (P4, P5, P18, P16, P14),
    (P5, P4, P3, P2, P1)
]


# Dibujar Caras..
def drawPentagons(caras, canvas):
    for p in caras:
        print("caras: ", p[0].x, p[0].y, p[0].z, " | ", p[1].x, p[1].y, p[1].z, " | ", p[2].x, p[2].y, p[2].z)
        gf.drawLine(gf.projectVertex(p[0], canvas), gf.projectVertex(p[1], canvas), BLUE, canvas)
        gf.drawLine(gf.projectVertex(p[1], canvas), gf.projectVertex(p[2], canvas), RED, canvas)
        gf.drawLine(gf.projectVertex(p[2], canvas), gf.projectVertex(p[3], canvas), YELLOW, canvas)
        gf.drawLine(gf.projectVertex(p[3], canvas), gf.projectVertex(p[4], canvas), RED, canvas)
        gf.drawLine(gf.projectVertex(p[4], canvas), gf.projectVertex(p[0], canvas), BLUE, canvas)


drawPentagons(caras, canvas)

# Definir los triangulos
# triangles = [(0,1,2,RED),(0,2,3,RED),(4,0,3,GREEN),(4,3,7,GREEN),(5,4,7,BLUE),(5,7,6,BLUE),
#             (1,5,6,YELLOW),(1,6,2,YELLOW),(4,5,1,PURPLE),(4,1,0,PURPLE),(2,6,7,CYAN),(2,7,3,CYAN)]

# Graficar los puntosrenderObject(vertices,triangles,canvas)

# Trazar Caras

##############################################################################################

canvas.show()
