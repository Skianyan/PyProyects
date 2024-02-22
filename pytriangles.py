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

def interpolate (i0,f0,i1,f1):
    if i0 == i1:
        return [f0]
    values = []
    a = (f1-f0)/(i1-i0)
    d = f0
    for i in range(i0, i1):
        values.append(d)
        d = d + a
    return values

def drawTriangle(p0, p1, p2, fill, edge, canvas):
    # Define correctamente los puntos
    if p0.x < p1.x:
        p0, p1 = p1, p0
        #x0, y0, x1, y1 = x1, y1, x0, y1
    if p0.x < p2.x:
        p0, p2 = p2, p0
        #x0, y0, x2, y2 = x2, y2, x0, y0
    if p1.x < p2.x:
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
    drawLine(p0, p1, edge, canvas)
    drawLine(p1, p2, edge, canvas)
    drawLine(p2, p0, edge, canvas)

    print("2-1 coords =",x2, y2, x1, y1)
    y1s = interpolate(x2, y2, x1, y1)
    print('y2-1 s =', y1s)

    print("1-0 coords =", x1, y1, x0, y0)
    y2s = interpolate(x1, y1, x0, y0)
    print('y1-0 s =', y2s)

    print("2-0 coords =", x2, y2, x0, y0)
    y3s = interpolate(x2, y2, x0, y0)
    print('y2-0 s =', y3s)

    y4s = y1s + y2s
    print('y0-1-2s =', y4s)


    # i in y4s:
        #drawLine(y3s[i], y4s[i], fill, canvas)


    return

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
            putPixel(int(xs[y-y0]), int(y), color, canvas)


# Tamaño de la imagen
width = 501
height = 501

# Definir un lienzo
canvas = Image.new('RGB', (width, height), (255, 255, 255))

# Definir los puntos
P1 = Pt(200, 90)
P2 = Pt(-200, -50)
P0 = Pt(50, -90)

# Definir los colores
color = (0, 0, 0)
fill = (160, 32, 240)

#Trazar las lineas
drawLine(P0, P1, color, canvas)
drawLine(P1, P2, color, canvas)
drawLine(P2, P0, color, canvas)

canvas.show()

drawTriangle(P0, P1, P2, fill, color, canvas)


# # Definir Triangulo Manualmente
# # Puntos iniciales
# P0 = Pt(200, 90)
# P1 = Pt(-200, -50)
# P2 = Pt(50, -90)
# # color de la linea
# color = (0, 0, 0)
# drawLine(P0, P1, color, canvas)
# drawLine(P1, P2, color, canvas)
# drawLine(P2, P0, color, canvas)

# canvas.save("linea.png")