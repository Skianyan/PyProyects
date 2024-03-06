import gfxlib as gf
from math import floor
from PIL import Image, ImageDraw


# #Program Loop
#
# print("1.- Define canvas size.")
#
# # Get Canvas Width
# width = gf.getIntValue("width", 500)
#
# # Get Canvas Height
# height = gf.getIntValue("height", 500)

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

# Graficar los puntos
gf.renderObject(vertices,triangles,canvas)
##############################################################################################

# Trazar Caras



# gf.drawLine(gf.projectVertex(vAf,canvas), gf.projectVertex(vBf,canvas), BLUE,canvas)
# gf.drawLine(gf.projectVertex(vBf,canvas), gf.projectVertex(vCf,canvas), BLUE,canvas)
# gf.drawLine(gf.projectVertex(vCf,canvas), gf.projectVertex(vDf,canvas), BLUE,canvas)
# gf.drawLine(gf.projectVertex(vDf,canvas), gf.projectVertex(vAf,canvas), BLUE,canvas)
#
# gf.drawLine(gf.projectVertex(vAb,canvas), gf.projectVertex(vBb,canvas), RED, canvas)
# gf.drawLine(gf.projectVertex(vBb,canvas), gf.projectVertex(vCb,canvas), RED, canvas)
# gf.drawLine(gf.projectVertex(vCb,canvas), gf.projectVertex(vDb,canvas), RED, canvas)
# gf.drawLine(gf.projectVertex(vDb,canvas), gf.projectVertex(vAb,canvas), RED, canvas)
#
# gf.drawLine(gf.projectVertex(vAf,canvas), gf.projectVertex(vAb,canvas), GREEN, canvas)
# gf.drawLine(gf.projectVertex(vBf,canvas), gf.projectVertex(vBb,canvas), GREEN, canvas)
# gf.drawLine(gf.projectVertex(vCf,canvas), gf.projectVertex(vCb,canvas), GREEN, canvas)
# gf.drawLine(gf.projectVertex(vDf,canvas), gf.projectVertex(vDb,canvas), GREEN, canvas)

canvas.show()
