from PIL import Image, ImageDraw

#punto a
class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#funcion para poner pixel
def putPixel (x,y,color,canvas):
    x=canvas.width/2 + x
    y=canvas.height/2 - y

    if (x < 0 or x >= canvas.width or y < 0 or y >= canvas.height):
        return
    canvas.putpixel((int(x),int(y)), color)

def drawLine (P0, P1, color, canvas):
    a = (P1.y - P0.y / (P1.x - P0.x))
    b = P0.y - a * P0.x

    for x in range(P0.x, P1.x):
        y=a*x+b
        putPixel(int(x), int(y), color, canvas)

#tama;o de imagen
width=501
height=501

#definir canvas
canvas = Image.new('RGB', (width,height), (255,255,255))

color = (150, 0, 150)

P0 = Pt(200, 300)
P1 = Pt(100, 150)

drawLine(P0, P1, color, canvas)

#P0=Pt(0,0)
#putPixel(P0.x,P0.y,color,canvas)


canvas.show()


#tarea, graficar una parabola
#
# def calcular_recta_entre_puntos(punto1, punto2):
#     # Calcular la pendiente
#     pendiente = (punto2[1] - punto1[1]) / (punto2[0] - punto1[0])
#
#     # Verificar si la pendiente es mayor a 45 grados
#     if abs(pendiente) <= 1:
#         # Intercambiar los puntos para obtener una pendiente más empinada
#         punto1, punto2 = punto2, punto1
#         pendiente = (punto2[1] - punto1[1]) / (punto2[0] - punto1[0])
#
#     # Calcular el punto de intersección y la ecuación de la recta
#     b = punto1[1] - pendiente * punto1[0]
#
#     # La ecuación de la recta es y = mx + b
#     ecuacion_recta = f"y = {pendiente}x + {b}"
#
#     return ecuacion_recta
#
#
# # Ejemplo de uso
# punto1 = (1, 3)
# punto2 = (5, 8)
# recta = calcular_recta_entre_puntos(punto1, punto2)
# print("Ecuación de la recta entre los puntos:", recta)