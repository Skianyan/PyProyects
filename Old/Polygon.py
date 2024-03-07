import math
from math import floor

from PIL import Image, ImageDraw

# A Point.
class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Pth:
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h

def putPixel(x, y, color, canvas):
    x = canvas.width / 2 + x
    y = canvas.height / 2 - y

    if (x < 0 or x >= canvas.width or y < 0 or y >= canvas.height):
        return
    canvas.putpixel((int(x), int(y)), color)

def interpolate (i0,f0,i1,f1):
    if i0 == i1:
        return [f0]
    values = []
    a = (f1-f0)/(i1-i0)
    f = f0
    for i in range(i0, i1 + 1):
        values.append(f)
        f = f + a
    return values

def drawPointTriangle(p0, p1, p2, fill, edge, canvas):
    # Define correctamente los puntos
    if p1.y < p0.y:
        p0, p1 = p1, p0
        #x0, y0, x1, y1 = x1, y1, x0, y1
    if p2.y < p0.y:
        p0, p2 = p2, p0
        #x0, y0, x2, y2 = x2, y2, x0, y0
    if p2.y < p1.y:
        p1, p2 = p2, p1
        #x1, y1, x2, y2 = x2, y2, x1, y1

    # Definir puntos para legibilidad
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y

    # Trazar las lineas del triangulo
    #drawLine(p0, p1, edge, canvas)
    #drawLine(p1, p2, edge, canvas)
    #drawLine(p2, p0, edge, canvas)

    x01 = interpolate(y0, x0, y1, x1)
    x02 = interpolate(y0, x0, y2, x2)
    x12 = interpolate(y1, x1, y2, x2)

    #print('x01 =', x01)
    #print('x02 =', x02)
    #print('x12 =', x12)

    x01.pop(-1)
    x012 = x01 + x12
    # print('x012 =', x012)
    # print(x012.__len__())
    # print(x02.__len__())

    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        xleft = x02
        xright = x012
    else:
        xleft = x012
        xright = x02

    for y in range(y0, y2 + 1):
        a = round(xleft[y - y0])
        b = round(xright[y - y0])
        for x in range(a, b):
            putPixel(x, y, fill, canvas)

def drawShadedTriangle(p0, p1, p2, fill, edge, canvas):
    # Define correctamente los puntos
    if p1.y < p0.y:
        p0, p1 = p1, p0
    if p2.y < p0.y:
        p0, p2 = p2, p0
    if p2.y < p1.y:
        p1, p2 = p2, p1

    # Definir los valores de sombreado
    h0 = p0.h
    h1 = p1.h
    h2 = p2.h

    # Definir puntos para legibilidad
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y

    x01 = interpolate(y0, x0, y1, x1)
    h01 = interpolate(y0, h0, y1, h1)
    x02 = interpolate(y0, x0, y2, x2)
    h02 = interpolate(y0, h0, y2, h2)
    x12 = interpolate(y1, x1, y2, x2)
    h12 = interpolate(y1, h1, y2, h2)

    # print('x01 =', x01)
    # print('x02 =', x02)
    # print('x12 =', x12)

    # Concatenate Short sides 'x'
    x01.pop(-1)
    x012 = x01 + x12

    # Concatenate short sides 'h'
    h01.pop(-1)
    h012 = h01 + h12

    # print('x012 =', x012)
    # print(x012.__len__())
    # print(x02.__len__())

    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        xleft = x02
        hleft = h02

        xright = x012
        hright = h012
    else:
        xleft = x012
        hleft = h012

        xright = x02
        hright = h02

    for y in range(y0, y2 + 1):
        xl = round(xleft[y - y0])
        xr = round(xright[y - y0])
        h_seg = interpolate(xl, hleft[y - y0], xr, hright[y - y0])

        for x in range(xl, xr):
            shadedColor0 = int(fill[0] * h_seg[x - xl])
            shadedColor1 = int(fill[1] * h_seg[x - xl])
            shadedColor2 = int(fill[2] * h_seg[x - xl])
            shadedColor = (shadedColor0, shadedColor1, shadedColor2)
            putPixel(x, y, shadedColor, canvas)

def drawShadedPolygon(points, fill, edge, canvas):
    p_cent = calcular_centroide(points)
    #print("centroide (x,y):", p_cent.x, p_cent.y, p_cent.h)
    n = len(points)
    #print("Cuantos puntos:", n)

    for current_point, next_point in zip(points, points[1:]):
        #print("cp", current_point.x, current_point.y, current_point.h)
        drawShadedTriangle(current_point, next_point, p_cent, fill, edge, canvas)
        drawLine(current_point, next_point, edge, canvas)

    if next_point == points[n - 1]:
        #print("cp", current_point.x, current_point.y, current_point.h)
        drawShadedTriangle(points[0], next_point, p_cent, fill, edge, canvas)
        drawLine(points[0], next_point, edge, canvas)
    return

def drawPolygon(points, fill, edge, canvas):
    cent = calcular_centroide(points)
    #print("centroide (x,y):", cent.x, cent.y)
    n = len(points)
    #print("Cuantos puntos:", n)

    for current_point, next_point in zip(points, points[1:]):
        #print("cp", current_point.x, current_point.y)
        drawPointTriangle(current_point, next_point, cent, fill, edge, canvas)
        drawLine(current_point, next_point, edge, canvas)

    if next_point == points[n-1]:
        #print("cp", current_point.x, current_point.y)
        drawPointTriangle(points[0], next_point, cent, fill, edge, canvas)
        drawLine(points[0], next_point, edge, canvas)

    drawPointTriangle(points[0],points[1], cent, fill, edge, canvas)
    return

def calcular_centroide(puntos):
    n = len(puntos)

    sum_x = sum(point.x for point in puntos)
    sum_y = sum(point.y for point in puntos)
    sum_h = sum(point.h for point in puntos)

    centroide_x = int(sum_x / n)
    centroide_y = int(sum_y / n)
    centroide_h = sum_h / n
    cent = Pth(centroide_x, centroide_y, centroide_h)
    return cent

def drawLine(p0, p1, color, canvas):
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y

    if abs(x1 - x0) > abs(y1 - y0):
        # Es una linea horizontal
        if x0 > x1:
            x0, x1, y0, y1 = x1, x0, y1, y0
        ys = interpolate(x0, y0, x1, y1)
        for x in range(x0, x1):
            putPixel(int(x), int(ys[x-x0]), color, canvas)
    else:
        # Es una linea vertical
        if y0 > y1:
            x0, x1, y0, y1 = x1, x0, y1, y0

        xs = interpolate(y0, x0, y1, x1)

        for y in range(y0, y1):
            putPixel(int(xs[y-y0]), int(y), color, canvas);

#############################################################################

# Helper Functions

def getIntValue(value, min):
    try:
        value = int(input("Define " + value + ": "))
    except ValueError:
        print('Enter a valid integer')
    if value < min:
        print("Please enter a number larger than " + str(min))

        exit()
    return value


##############################################################################################

#Program Loop

print("1.- Define canvas size.")

# Get Canvas Width
width = getIntValue("width", 500)

# Get Canvas Height
height = getIntValue("height", 500)

##############################################################################################

# Definir un lienzo
canvas = Image.new('RGB', (int(width), int(height)), (255, 255, 255))

# Ejemplo de uso, poligono
puntos = [Pth(-200, -200, 1), Pth(-100, 80, .9), Pth(170, 170, .6), Pth(150, -50, .4), Pth(0,-200, .1)]

# Definir los colores
color = (0, 0, 0)
fill = (160, 32, 240)

drawShadedPolygon(puntos, fill, color, canvas)
canvas.show()

## definir el centroide h como el promedio de las h igual que el centroide de x, y