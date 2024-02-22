from PIL import Image

def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def point_in_triangle(pt, v1, v2, v3):
    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0
    return (b1 == b2) and (b2 == b3)

def fill_triangle(image, v1, v2, v3, color):
    bbox = [min(v1[0], v2[0], v3[0]), min(v1[1], v2[1], v3[1]),
            max(v1[0], v2[0], v3[0]), max(v1[1], v2[1], v3[1])]

    for x in range(bbox[0], bbox[2] + 1):
        for y in range(bbox[1], bbox[3] + 1):
            if point_in_triangle((x, y), v1, v2, v3):
                image.putpixel((x, y), color)

# Example usage:
image = Image.new("RGB", (500, 500), "white")
fill_triangle(image, (100, 100), (200, 300), (300, 200), (255, 0, 0))
image.show()