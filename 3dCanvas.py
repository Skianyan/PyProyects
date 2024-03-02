import graphlib as gf
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
vAf = gf.Vertex(-200, -50.5, 50)
vBf = gf.Vertex(-200, -50.5, 50)
vCf = gf.Vertex(-100, -50.5, 50)
vDf = gf.Vertex(-100, -50.5, 50)

# Definir Vertices posteriores
vAb = gf.Vertex(-200, -50.5, 60)
vBb = gf.Vertex(-200, -50.5, 60)
vCb = gf.Vertex(-100, -50.5, 60)
vDb = gf.Vertex(-100, -50.5, 60)

# Definir los colores
BLUE = (10, 10, 255)

##############################################################################################

# Trazar Caras

gf.drawLine(gf.proyectVertex(vAf, canvas), gf.proyectVertex(vBf, canvas), BLUE, canvas)
gf.drawLine(gf.proyectVertex(vBf, canvas), gf.proyectVertex(vCf, canvas), BLUE, canvas)
gf.drawLine(gf.proyectVertex(vCf, canvas), gf.proyectVertex(vDf, canvas), BLUE, canvas)
gf.drawLine(gf.proyectVertex(vDf, canvas), gf.proyectVertex(vAf, canvas), BLUE, canvas)

canvas.show()
