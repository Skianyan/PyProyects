import math
import numpy as np


# A Point.
class Pt:
    def __init__(self, x, y, h=1):
        self.x = x
        self.y = y
        self.h = h


# Model Class
class Model:
    def __init__(self, vertices, triangles):
        self.vertices = vertices
        self.triangles = triangles

class Camera:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
class Instance:
    def __init__(self, model, position, orientation, scale=1):
        self.model = model
        self.position = position
        self.orientation = orientation
        self.scale = scale

        self.transform = MultiplyMM4(MakeTranslationMatrix(self.position), MultiplyMM4(MakeScalingMatrix(self.scale), MultiplyMM4(identity4x4, MakeRotationMatrix(self.orientation))))

    def apply_camera_transform(self, camera):
        # Calculate the inverse camera transformation
        invcam = inv_camera_transform(camera)

        # Apply the inverse camera transformation to the object's transform
        self.transform = MultiplyMM4(self.transform, invcam)

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

def inv_camera_transform(camera):
    # Calculate inverse translation matrix
    inv_translation = MakeTranslationMatrix(Vertex(-camera.position.x, -camera.position.y, -camera.position.z))

    # Calculate inverse rotation matrix
    inv_rotation = MakeRotationMatrix(Vertex(-camera.orientation.x, -camera.orientation.y, -camera.orientation.z))

    # Multiply inverse translation and rotation matrices
    inv_camera_transform = MultiplyMM4(inv_translation, inv_rotation)

    return inv_camera_transform
##########################################
# Calculation Functions


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def is_rgb(color):
    if not isinstance(color, tuple):
        return False
    if len(color) != 3:
        return False
    for component in color:
        if not isinstance(component, int):
            return False
        if component < 0 or component > 255:
            return False
    return True

def putPixel(x, y, color, canvas):
    x = canvas.winfo_reqwidth() / 2 + x
    y = canvas.winfo_reqheight() / 2 - y
    if is_rgb(color):
        color = rgb_to_hex(color[0],color[1],color[2])
    canvas.create_rectangle(x, y, x + 1, y + 1, outline=color)

def interpolate(i0, d0, i1, d1):
    if i0 == i1:
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

def projectVertex(V, canvas):
    projection_plane_z = 1
    xp = V.x * projection_plane_z / V.z
    yp = V.y * projection_plane_z / V.z
    pp = Pt(xp, yp)
    return viewportToCanvas(pp, canvas)


def viewportToCanvas(P2d, canvas):
    viewport_size = 1
    return Pt(int(P2d.x * canvas.winfo_reqwidth() / viewport_size) | 0, int(P2d.y * canvas.winfo_reqheight() / viewport_size) | 0)


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
