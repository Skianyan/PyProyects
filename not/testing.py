import math
from PIL import Image, ImageDraw


# A Point.
class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# The putPixel() function.
def putPixel(x, y, color, canvas):
    x = canvas.width / 2 + x
    y = canvas.height / 2 - y

    if (x < 0 or x >= canvas.width or y < 0 or y >= canvas.height):
        return
    canvas.putpixel((int(x), int(y)), color)


def interpolate(i0, d0, i1, d1):
    if (i0 == i1):
        return [d0]

    values = []
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0, i1 + 1):
        values.append(d)
        d += a

    return values


def drawLine(p0, p1, color, canvas):
    dx = p1.x - p0.x
    dy = p1.y - p0.y

    if (abs(dx) > abs(dy)):
        # The line is horizontal-ish. Make sure it's left to right.
        if (dx < 0):
            p0, p1 = p1, p0

        # Compute the Y values and draw.
        ys = interpolate(p0.x, p0.y, p1.x, p1.y)
        for x in range(p0.x, p1.x):
            putPixel(x, ys[(x - p0.x) | 0], color, canvas)

    else:
        # The line is verical-ish. Make sure it's bottom to top.
        if (dy < 0):
            p0, p1 = p1, p0

        # Compute the X values and draw.
        xs = interpolate(p0.y, p0.x, p1.y, p1.x)
        for y in range(p0.y, p1.y):
            putPixel(xs[(y - p0.y) | 0], y, color, canvas)


def drawWireframeTriangle(P0, P1, P2, color, canvas):
    drawLine(P0, P1, color, canvas)
    drawLine(P1, P2, color, canvas)
    drawLine(P2, P0, color, canvas)


def drawFilledTriangle(P0, P1, P2, color, canvas):
    # Sort the points so that y0 <= y1 <= y2

    if P1.y < P0.y:
        P0, P1 = P1, P0
    if P2.y < P0.y:
        P0, P2 = P2, P0
    if P2.y < P1.y:
        P1, P2 = P2, P1

        # Compute the x coordinates of the triangle edges
    x01 = interpolate(P0.y, P0.x, P1.y, P1.x)
    x12 = interpolate(P1.y, P1.x, P2.y, P2.x)
    x02 = interpolate(P0.y, P0.x, P2.y, P2.x)

    # Concatenate the short sides
    # remove_last(x01)
    x01.pop(-1)
    x012 = x01 + x12

    # Determine which is left and which is right
    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        x_left = x02
        x_right = x012
    else:
        x_left = x012
        x_right = x02

    # Draw the horizontal segments
    for y in range(P0.y, P2.y + 1):
        a = round(x_left[y - P0.y])
        b = round(x_right[y - P0.y])
        for x in range(a, b):
            putPixel(x, y, color, canvas)


# Tamaño de la imagen
width = 501
height = 501

# Definir un lienzo
canvas = Image.new('RGB', (width, height), (255, 255, 255))

# Puntos iniciales
P0 = Pt(-200, -200)
P1 = Pt(-50, 80)
P2 = Pt(170, 170)
# color de la linea
color = (0, 0, 0)

# dibujar el contorno
drawWireframeTriangle(P0, P1, P2, color, canvas)

# iluminar el polígono
color = (255, 100, 255)
drawFilledTriangle(P0, P1, P2, color, canvas)

canvas.show()
