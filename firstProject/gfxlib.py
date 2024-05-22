import math
import numpy as np


# A Point.
class Pt:
    def __init__(self, x, y, h=1):
        self.x = x
        self.y = y
        self.h = h

class Plane:
    def __init__(self,normal,distance):
        self.normal = normal
        self.distance = distance

# Model Class
class Model:
    def __init__(self, vertices, triangles):
        self.vertices = vertices
        self.triangles = triangles


class Instance:
    def __init__(self, model, position, orientation, scale=1):
        self.model = model
        self.position = position
        self.orientation = orientation
        self.scale = scale

        self.transform = MultiplyMM4(MakeTranslationMatrix(self.position), MultiplyMM4(MakeScalingMatrix(self.scale), MultiplyMM4(identity4x4, MakeRotationMatrix(self.orientation))))

class Camera:
    def __init__(self, position, orientation, clipping_planes):
        self.position = position
        self.orientation = orientation
        self.clipping_planes = clipping_planes
class Inst2:
    def __init__(self, model, transform):
        self.model = model
        self.transform = transform

class Mat4x4:
    def __init__(self, data):
        self.data = data


def MultiplyMM4(matA, matB):
    result = Mat4x4([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    for i in range(0, 4):
        for j in range(0, 4):
            for k in range(0, 4):
                result.data[i][j] += matA.data[i][k] * matB.data[k][j]

    return result


identity4x4 = Mat4x4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

def ApplyTransform(vertex, transform):
    scaled = MakeScalingMatrix(vertex, transform.scale)
    rotated = MakeRotationMatrix(scaled, transform.orientation)
    translated = MakeTranslationMatrix(rotated, transform.position)
    return translated

def MultiplyMV(mat4x4, vec4):
    result = [0, 0, 0, 0]
    vec = [vec4.x, vec4.y, vec4.z, vec4.w]

    for i in range(0, 4):
        for j in range(0, 4):
            result[i] += mat4x4.data[i][j] * vec[j]

    return Vertex(result[0], result[1], result[2], result[3])


# A 3D vertex.
class Vertex:
    def __init__(self, x, y, z, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w


class Triangle:
    def __init__(self, indexes, color):
        self.indexes = indexes
        self.color = color


# The putPixel() function.
def MakeTranslationMatrix(translation):
    return Mat4x4([[1, 0, 0, translation.x], [0, 1, 0, translation.y], [0, 0, 1, translation.z], [0, 0, 0, 1]])


def MakeScalingMatrix(scale):
    return Mat4x4([[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]])


def MakeRotationMatrix(rotation):
    MatRx = Mat4x4([[1, 0, 0, 0], [0, math.cos(rotation.x), -math.sin(rotation.x), 0], [0, math.sin(rotation.x), math.cos(rotation.x), 0], [0, 0, 0, 1]])

    MatRy = Mat4x4([[math.cos(rotation.y), 0, math.sin(rotation.y), 0], [0, 1, 0, 0], [-math.sin(rotation.y), 0, math.cos(rotation.y), 0], [0, 0, 0, 1]])

    MatRz = Mat4x4([[math.cos(rotation.z), -math.sin(rotation.z), 0, 0], [math.sin(rotation.z), math.cos(rotation.z), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    RotMat = MultiplyMM4(MatRx, MultiplyMM4(MatRz, MatRy))
    return RotMat


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


def drawShadedTriangle(P0, P1, P2, color, canvas):
    # Sort the points so that y0 <= y1 <= y2

    if P1.y < P0.y:
        P0, P1 = P1, P0
    if P2.y < P0.y:
        P0, P2 = P2, P0
    if P2.y < P1.y:
        P1, P2 = P2, P1

    # Compute the x coordinates of the triangle edges
    x01 = interpolate(P0.y, P0.x, P1.y, P1.x)
    h01 = interpolate(P0.y, P0.h, P1.y, P1.h)

    x12 = interpolate(P1.y, P1.x, P2.y, P2.x)
    h12 = interpolate(P1.y, P1.h, P2.y, P2.h)

    x02 = interpolate(P0.y, P0.x, P2.y, P2.x)
    h02 = interpolate(P0.y, P0.h, P2.y, P2.h)

    # Concatenate the short sides
    # remove_last(x01)
    x01.pop(-1)
    x012 = x01 + x12

    h01.pop(-1)
    h012 = h01 + h12

    # Determine which is left and which is right
    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        x_left = x02
        h_left = h02

        x_right = x012
        h_right = h012
    else:
        x_left = x012
        h_left = h012

        x_right = x02
        h_right = h02

    # Draw the horizontal segments
    for y in range(P0.y, P2.y + 1):
        xl = round(x_left[y - P0.y])
        hl = h_left[y - P0.y]

        xr = round(x_right[y - P0.y])
        hr = h_right[y - P0.y]

        h_segment = interpolate(xl, hl, xr, hr)

        for x in range(xl, xr):
            sh_color0 = round(color[0] * h_segment[x - xl])
            sh_color1 = round(color[1] * h_segment[x - xl])
            sh_color2 = round(color[2] * h_segment[x - xl])
            shaded_color = (sh_color0, sh_color1, sh_color2)

            putPixel(x, y, shaded_color, canvas)


def calc_centroide(puntos):
    n = len(puntos)

    sum_x = sum(point.x for point in puntos)
    sum_y = sum(point.y for point in puntos)

    centroide_x = int(sum_x / n)
    centroide_y = int(sum_y / n)

    cent = Pt(centroide_x, centroide_y)
    return cent


def projectVertex(V, canvas):
    projection_plane_z = 1
    xp = V.x * projection_plane_z / V.z
    yp = V.y * projection_plane_z / V.z
    pp = Pt(xp, yp)
    return viewportToCanvas(pp, canvas)


def viewportToCanvas(P2d, canvas):
    viewport_size = 1
    return Pt(int(P2d.x * canvas.width / viewport_size) | 0, int(P2d.y * canvas.height / viewport_size) | 0)


def renderObject(vertices, triangles, canvas):
    projected = []
    for V in vertices:
        projected.append(projectVertex(V, canvas))
    for T in triangles:
        renderTriangle(T, projected, canvas)


def renderTriangle(triangle, projected, canvas):
    drawWireframeTriangle(projected[triangle[0]],
                          projected[triangle[1]],
                          projected[triangle[2]],
                          triangle[3], canvas)


##########################################################
# Dodecahedron....

def pent_triangles(p, color):
    cent = calc_centroide(p)
    triangles = [[p[0], p[1], cent], [p[1], p[2], cent], [p[2], p[3], cent], [p[3], p[4], cent],
                 [p[4], p[0], cent], color]
    return triangles


def pentagons_to_triangles(pentagons):
    for p in pentagons:
        cent = calc_centroide(p)
        triangles = [(p[0], p[1], cent), (p[1], p[2], cent), (p[2], p[3], cent), (p[3], p[4], cent),
                     (p[4], p[0], cent)]
    return triangles
