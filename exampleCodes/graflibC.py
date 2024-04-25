import math
import numpy as np


# A Point.
class Pt:
    def __init__(self, x, y, h=1):
        self.x = x
        self.y = y
        self.h = h


# A 3D vertex.
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


# A 4D vertex (a 3D vertex in homogeneous coordinates).
class Vertex4:
    def __init__(self, arg1, y=0, z=0, w=0):
        if isinstance(arg1, Vertex):
            self.x = arg1.x
            self.y = arg1.y
            self.z = arg1.z
            self.w = 1

        elif isinstance(arg1, Vertex4):
            self.x = arg1.x
            self.y = arg1.y
            self.z = arg1.z
            self.w = arg1.w
        else:
            self.x = arg1
            self.y = y
            self.z = z
            self.w = w


class Triangle:
    def __init__(self, indexes, color):
        self.indexes = indexes
        self.color = color


# A Model.
class Model:
    def __init__(self, vertices, triangles, bounds_center, bounds_radius):
        self.vertices = vertices
        self.triangles = triangles
        self.bounds_center = bounds_center
        self.bounds_radius = bounds_radius


# An Instance.
class Instance:
    def __init__(self, model, position=0, orientation=[0, 0, 0], scale=1.0):
        # Modelo (Vertices y Triangulos)
        self.model = model
        # Traslación
        self.position = position
        # Rotación
        self.orientation = orientation
        # Escala
        self.scale = scale

        # Matriz de transformación
        self.transform = MultiplyMM4(MakeTranslationMatrix(self.position),
                                     MultiplyMM4(self.orientation, MakeScalingMatrix(self.scale)))


# The Camera.
class Camera:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.clipping_planes = []


# A Clipping Plane.
class Plane:
    def __init__(self, normal, distance):
        self.normal = normal
        self.distance = distance


# A 4x4 matrix.
class Mat4x4:
    def __init__(self, data):
        self.data = data


# ======================================================================
#    Linear algebra and helpers.
# ======================================================================

# Constantes
Identity4x4 = Mat4x4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


# Computes k * vec.
def Multiply(k, vec):
    return Vertex(k * vec.x, k * vec.y, k * vec.z)


# Computes dot product.
def Dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


# Computes cross product.
def Cross(v1, v2):
    return Vertex(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x)


# Computes v1 + v2.
def Add(v1, v2):
    return Vertex(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)


# Computes vector magnitude.
def Magnitude(v1):
    return math.sqrt(Dot(v1, v1))


# Makes a transform matrix for a rotation around the OY axis.
def MakeOYRotationMatrix(degrees):
    cos = math.cos(degrees * math.pi / 180.0)
    sin = math.sin(degrees * math.pi / 180.0)

    return Mat4x4([[cos, 0, -sin, 0],
                   [0, 1, 0, 0],
                   [sin, 0, cos, 0],
                   [0, 0, 0, 1]])


# Makes a transform matrix for a translation.
def MakeTranslationMatrix(translation):
    return Mat4x4([[1, 0, 0, translation.x],
                   [0, 1, 0, translation.y],
                   [0, 0, 1, translation.z],
                   [0, 0, 0, 1]])


# Makes a transform matrix for a scaling.
def MakeScalingMatrix(scale):
    return Mat4x4([[scale, 0, 0, 0],
                   [0, scale, 0, 0],
                   [0, 0, scale, 0],
                   [0, 0, 0, 1]])


# Multiplies a 4x4 matrix and a 4D vector.
def MultiplyMV(mat4x4, vec4):
    result = [0, 0, 0, 0]
    vec = [vec4.x, vec4.y, vec4.z, vec4.w]

    for i in range(0, 4):
        for j in range(0, 4):
            result[i] += mat4x4.data[i][j] * vec[j]

    return Vertex4(result[0], result[1], result[2], result[3])


# Multiplies two 4x4 matrices.
def MultiplyMM4(matA, matB):
    result = Mat4x4([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    for i in range(0, 4):
        for j in range(0, 4):
            for k in range(0, 4):
                result.data[i][j] += matA.data[i][k] * matB.data[k][j]

    return result


# Transposes a 4x4 matrix.
def Transposed(mat):
    result = Mat4x4([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    for i in range(0, 4):
        for j in range(0, 4):
            result.data[i][j] = mat.data[j][i]

    return result


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
    for i in range(int(i0), i1 + 1):
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


def ComputeTriangleNormal(vertex1, vertex2, vertex3):
    # Calculate the vectors representing the two edges of the triangle
    edge1 = np.array(vertex2) - np.array(vertex1)
    edge2 = np.array(vertex3) - np.array(vertex1)

    # Compute the cross product of the edges to get the normal vector
    normal = np.cross(edge1, edge2)

    # Normalize the normal vector to unit length
    normal /= np.linalg.norm(normal)

    return tuple(normal)


def EdgeInterpolate(y0, x0, y1, x1, y2, x2):
    # Calculate the slopes of the attributes
    slope0 = (x2 - x0) / (y2 - y0)
    slope1 = (x2 - x1) / (y2 - y1)

    # Interpolate values at the start and end points of the edge
    val0 = x0 + slope0 * (y1 - y0)
    val1 = x1 + slope1 * (y2 - y1)

    return val0, val1

def UpdateDepthBufferIfCloser(depth_buffer, x, y, inv_z):
    if x < 0 or x >= len(depth_buffer) or y < 0 or y >= len(depth_buffer[0]):
        return False

    if inv_z <= depth_buffer[x][y]:
        depth_buffer[x][y] = inv_z
        return True

    return False


def MultiplyColor(color, intensity):
    # Multiplication of color components with an intensity factor
    multiplied_color = tuple(int(c * intensity) for c in color)

    return multiplied_color


def SortedVertexIndexes(vertex_indexes, projected_vertices):
    # Sort the vertex indexes based on the projected Y-coordinates of the vertices
    sorted_indexes = sorted(vertex_indexes, key=lambda i: projected_vertices[i].y)

    return sorted_indexes

def renderTriangleDepth(triangle, vertices, projected, canvas, depth_buffer= 0, intensity = 1):
    # Sort by projected point Y.
    indexes = SortedVertexIndexes(triangle.indexes, projected)
    i0, i1, i2 = indexes[0], indexes[1], indexes[2]

    v0 = vertices[triangle.indexes[i0]]
    v1 = vertices[triangle.indexes[i1]]
    v2 = vertices[triangle.indexes[i2]]

    # Compute triangle normal. Use the unsorted vertices, otherwise the winding of the points may change.
    normal = ComputeTriangleNormal(vertices[triangle.indexes[0]], vertices[triangle.indexes[1]],
                                   vertices[triangle.indexes[2]])

    # Backface culling.
    vertex = vertices[triangle.indexes[0]]
    if Dot(vertex, normal) >= 0:
        return

    # Get attribute values (X, 1/Z) at the vertices.
    p0 = projected[triangle.indexes[i0]]
    p1 = projected[triangle.indexes[i1]]
    p2 = projected[triangle.indexes[i2]]

    # Compute attribute values at the edges.
    x02, x012 = EdgeInterpolate(p0.y, p0.x, p1.y, p1.x, p2.y, p2.x)
    iz02, iz012 = EdgeInterpolate(p0.y, 1.0 / v0.z, p1.y, 1.0 / v1.z, p2.y, 1.0 / v2.z)

    # Determine which is left and which is right.
    m = int(len(x02) / 2) | 0
    if x02[m] < x012[m]:
        x_left, x_right = x02, x012
        iz_left, iz_right = iz02, iz012

    else:
        x_left, x_right = x012, x02
        iz_left, iz_right = iz012, iz02

    # Draw horizontal segments.
    for y in range(p0.y, p2.y + 1):
        xl, xr = int(x_left[y - p0.y]) | 0, int(x_right[y - p0.y]) | 0

        # Interpolate attributes for self scanline.
        zl, zr = iz_left[y - p0.y], iz_right[y - p0.y]
        zscan = interpolate(xl, zl, xr, zr)
        for x in range(xl, xr):
            inv_z = zscan[x - xl]
            if UpdateDepthBufferIfCloser(canvas, depth_buffer, x, y, inv_z):
                putPixel(canvas, x, y, MultiplyColor(triangle.color, intensity))



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


def projectVertex(V, canvas):
    projection_plane_z = 1
    xp = V.x * projection_plane_z / V.z
    yp = V.y * projection_plane_z / V.z
    Pp = Pt(xp, yp)

    return viewportToCanvas(Pp, canvas)


def viewportToCanvas(P2d, canvas):
    viewport_size = 1

    return Pt(int(P2d.x * canvas.width / viewport_size) | 0, int(P2d.y * canvas.height / viewport_size) | 0)


def renderObject(vertices, triangles, canvas):
    projected = []
    for V in vertices:
        projected.append(projectVertex(V, canvas))
    for T in triangles:
        renderTriangle(T, projected, canvas)


def renderTriangleOld(triangle, projected, canvas):
    # Get attribute values (X, 1/Z) at the vertices.
    p0 = projected[triangle.indexes[0]]
    p1 = projected[triangle.indexes[1]]
    p2 = projected[triangle.indexes[2]]

    renderTriangleDepth(p0, p1, p2, triangle.color, canvas)


def renderTriangle(triangle, projected, canvas):
    # Get attribute values (X, 1/Z) at the vertices.
    p0 = projected[triangle.indexes[0]]
    p1 = projected[triangle.indexes[1]]
    p2 = projected[triangle.indexes[2]]

    drawShadedTriangle(p0, p1, p2, triangle.color, canvas)


def IntersectPlane(plane, p0, p1):
    # Compute the direction vector of the line segment.
    direction = Vertex(p1.x - p0.x, p1.y - p0.y, p1.z - p0.z)

    # Compute the parameter t at which the line intersects the plane.
    t = -(Dot(plane.normal, p0) + plane.distance) / Dot(plane.normal, direction)

    # Compute the intersection point.
    intersection_point = Vertex(p0.x + t * direction.x, p0.y + t * direction.y, p0.z + t * direction.z)

    return intersection_point
