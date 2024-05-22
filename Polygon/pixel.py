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


def drawLine(p0, p1, color, canvas):
    dx = p1.x - p0.x
    dy = p1.y - p0.y

    if dx < 0:
        p0,p1 = p1,p0

    if dx < dy:
        a = dx / dy
        # b = p0.y - a*p0.x
        x = p0.x
        for y in range(p0.y, p1.y):
            # y=a*x+b
            x = x + a
            putPixel(int(x), int(y), color, canvas)

    else:
        a = dy / dx
        # b = p0.y - a*p0.x
        y = p0.y
        for x in range(p0.x, p1.x):
            # y=a*x+b
            y = y + a
            putPixel(int(x), int(y), color, canvas)


# Tamaño de la imagen
width = 501
height = 501

# Definir un lienzo
canvas = Image.new('RGB', (width, height), (255, 255, 255))

# Puntos iniciales
P0 = Pt(100, -200)
P1 = Pt(200, 200)
# color de la linea
color = (0, 0, 0)

drawLine(P0, P1, color, canvas)
canvas.show()