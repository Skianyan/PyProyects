import gfxlib as gf
from math import floor
from PIL import Image, ImageDraw

width = 501
height = 501

##############################################################################################

# Definir un lienzo
canvas = Image.new('RGB', (int(width), int(height)), (255, 255, 255))

# Definir Vertices frontales
vAf = gf.Vertex(.5, -0.5, -0.5)
vBf = gf.Vertex(.5, 0.5, -0.5)
vCf = gf.Vertex(-.5, 0.5, -0.5)
vDf = gf.Vertex(-.5, -0.5, -0.5)

# Definir Vertices posteriores
vAb = gf.Vertex(.5, -0.5, 0.5)
vBb = gf.Vertex(.5, 0.5, 0.5)
vCb = gf.Vertex(-.5, 0.5, 0.5)
vDb = gf.Vertex(-.5, -0.5, 0.5)

# Juntar los vertices en una lista
vertices = []
vertices.append(vAf), vertices.append(vBf), vertices.append(vCf), vertices.append(vDf),
vertices.append(vAb), vertices.append(vBb), vertices.append(vCb), vertices.append(vDb)

# Definir los colores
BLUE = (10, 10, 255)
RED = (255, 10, 10)
GREEN = (10, 255, 10)
YELLOW = (238, 232, 170)
PURPLE = (186, 85, 211)
CYAN = (0, 255, 255)

# Definir los triangulos
triangles = [(0, 1, 2, RED), (0, 2, 3, RED), (4, 0, 3, GREEN), (4, 3, 7, GREEN), (5, 4, 7, BLUE), (5, 7, 6, BLUE),
             (1, 5, 6, YELLOW), (1, 6, 2, YELLOW), (4, 5, 1, PURPLE), (4, 1, 0, PURPLE), (2, 6, 7, CYAN),
             (2, 7, 3, CYAN)]

cube = gf.Model(vertices, triangles)


# Graficar los puntos
# gf.renderObject(cube.vertices, cube.triangles, canvas)


# Instances Test

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

#6.31 for a full 360` ???

instances = [gf.Instance(cube, gf.Vertex(0, 1.5, 10), gf.Vertex(0, 0, 0),  1),
             gf.Instance(cube, gf.Vertex(0, 3, 10), gf.Vertex(0, 0, 0),  1),
             gf.Instance(cube, gf.Vertex(0, -1.5, 10), gf.Vertex(0, 0, 0), 1),
             gf.Instance(cube, gf.Vertex(0, -3, 10), gf.Vertex(0, 0, 0), 1),
             gf.Instance(cube, gf.Vertex(1.5, 0, 10), gf.Vertex(0, 0, 0), 1),
             gf.Instance(cube, gf.Vertex(3, 0, 10), gf.Vertex(0, 0, 0), 1),
             gf.Instance(cube, gf.Vertex(-1.5, 0, 10), gf.Vertex(0, 0, 0), 1),
             gf.Instance(cube, gf.Vertex(-3, 0, 10), gf.Vertex(0, 0, 0), 1),
             gf.Instance(cube, gf.Vertex(0, 0, 10), gf.Vertex(15, 0, 0), 1)]

renderScene(instances, canvas)

##############################################################################################

# Trazar Caras

canvas.show()
