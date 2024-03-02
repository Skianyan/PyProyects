from PIL import Image, ImageDraw


def draw_line_between_points(image, point1, point2):
    draw = ImageDraw.Draw(image)
    draw.line((point1, point2), fill="black", width=2)
    image.show()


def swap_coordinates(point):
    return (point[1], point[0])


def plot_line(point1, point2):
    # Si la pendiente es mayor a 45 grados, intercambiar las coordenadas x e y
    if abs(point2[1] - point1[1]) > abs(point2[0] - point1[0]):
        point1 = swap_coordinates(point1)
        point2 = swap_coordinates(point2)

    # Crear una imagen
    width = 500
    height = 500
    image = Image.new("RGB", (width, height), "white")

    # Dibujar la línea entre los puntos
    draw_line_between_points(image, point1, point2)


# Puntos de ejemplo
point1 = (100, 0)
point2 = (200, 300)

plot_line(point1, point2)