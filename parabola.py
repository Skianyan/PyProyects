from PIL import Image, ImageDraw

class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def putPixel(x, y, color, canvas):
    x = int(canvas.width / 2 + x)
    y = int(canvas.height / 2 - y)

    if (x < 0 or x >= canvas.width or y < 0 or y >= canvas.height):
        return
    canvas.putpixel((x, y), color)

def drawParabola(a, b, c, color, canvas):
    for x in range(-canvas.width // 2, canvas.width // 2):
        y = a * x**2 + b * x + c
        putPixel(x, y, color, canvas)

# Tamaño de la imagen
width = 501
height = 501

# Definir canvas
canvas = Image.new('RGB', (width, height), (255, 255, 255))

# Color de la parábola
color = (150, 0, 150)

# Coeficientes de la parábola
a = 0.01
b = 0
c = 100

drawParabola(a, b, c, color, canvas)

canvas.show()