import gfxlib as gf
from math import floor
from PIL import Image, ImageDraw

width = 501
height = 501

##############################################################################################

# Definir un lienzo
canvas = Image.new('RGB', (int(width), int(height)), (255, 255, 255))

# Definir Vertices frontales
vAf = gf.Vertex(2, -0.5, 5)
vBf = gf.Vertex(2,  0.5, 5)
vCf = gf.Vertex(1,  0.5, 5)
vDf = gf.Vertex(1, -0.5, 5)

# Definir Vertices posteriores
vAb = gf.Vertex(2, -0.5, 6)
vBb = gf.Vertex(2,  0.5, 6)
vCb = gf.Vertex(1,  0.5, 6)
vDb = gf.Vertex(1, -0.5, 6)

# Juntar los vertices en una lista
vertices = []
vertices.append(vAf),vertices.append(vBf),vertices.append(vCf),vertices.append(vDf)
vertices.append(vAb),vertices.append(vBb),vertices.append(vCb),vertices.append(vDb),

# Definir los colores
BLUE = (10,10,255)
RED = (255,10,10)
GREEN = (10,255,10)
YELLOW = (238,232,170)
PURPLE = (186,85,211)
CYAN = (0,255,255)

# Definir los triangulos
triangles = [(0,1,2,RED),(0,2,3,RED),(4,0,3,GREEN),(4,3,7,GREEN),(5,4,7,BLUE),(5,7,6,BLUE),
             (1,5,6,YELLOW),(1,6,2,YELLOW),(4,5,1,PURPLE),(4,1,0,PURPLE),(2,6,7,CYAN),(2,7,3,CYAN)]

cube = gf.Model(vertices, triangles)

# Graficar los puntos
gf.renderObject(cube.vertices,cube.triangles,canvas)
##############################################################################################

# Trazar Caras

canvas.show()
