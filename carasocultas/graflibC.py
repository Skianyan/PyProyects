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


class Light:
    def __init__(self, type, intensity, vector=(0,0,0)):
        self.type = type
        self.intensity = intensity
        self.vector = vector


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
            putPixel(x, ys[(x - p0.x)], color, canvas)

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


# ======================================================================
#    Depth buffer.
# ======================================================================

def UpdateDepthBufferIfCloser(canvas, depth_buffer, x, y, inv_z):
    x = canvas.width / 2 + (x)
    y = canvas.height / 2 - (y) - 1

    if (x < 0 or x >= canvas.width or y < 0 or y >= canvas.height):
        return False

    offset = x + canvas.width * y
    if (depth_buffer[int(offset)] == None or depth_buffer[int(offset)] < inv_z):
        depth_buffer[int(offset)] = inv_z
        return True

    return False


def renderTriangle(triangle, projected, canvas):
    # Get attribute values (X, 1/Z) at the vertices.
    p0 = projected[triangle.indexes[0]]
    p1 = projected[triangle.indexes[1]]
    p2 = projected[triangle.indexes[2]]

    # drawWireframeTriangle(p0,p1,p2,triangle.color,canvas)
    drawFilledTriangle(p0, p1, p2, triangle.color, canvas)


def SortedVertexIndexes(vertex_indexes, projected):
    indexes = [0, 1, 2]

    if (projected[vertex_indexes[indexes[1]]].y < projected[vertex_indexes[indexes[0]]].y):
        indexes[0], indexes[1] = indexes[1], indexes[0]

    if (projected[vertex_indexes[indexes[2]]].y < projected[vertex_indexes[indexes[0]]].y):
        indexes[0], indexes[2] = indexes[2], indexes[0]

    if (projected[vertex_indexes[indexes[2]]].y < projected[vertex_indexes[indexes[1]]].y):
        indexes[1], indexes[2] = indexes[2], indexes[1]

    return indexes


def ComputeTriangleNormal(v0, v1, v2):
    v0v1 = Add(v1, Multiply(-1, v0))
    v0v2 = Add(v2, Multiply(-1, v0))
    return Cross(v0v1, v0v2)


def EdgeInterpolate(y0, v0, y1, v1, y2, v2):
    v01 = interpolate(y0, v0, y1, v1)
    v12 = interpolate(y1, v1, y2, v2)
    v02 = interpolate(y0, v0, y2, v2)
    v01.pop()
    v012 = v01 + v12
    return v02, v012


def renderTriangleDepth(triangle, vertices, projected, depth_buffer, canvas, lights):
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
    # vertex = Multiply(-1,vertices[triangle.indexes[0]])
    if Dot(vertex, normal) >= 0:
        return

    # Get attribute values (X, 1/Z) at the vertices.
    p0 = projected[triangle.indexes[i0]]
    p1 = projected[triangle.indexes[i1]]
    p2 = projected[triangle.indexes[i2]]

    # Compute attribute values at the edges.
    x02, x012 = EdgeInterpolate(p0.y, p0.x, p1.y, p1.x, p2.y, p2.x)
    iz02, iz012 = EdgeInterpolate(p0.y, 1.0 / v0.z, p1.y, 1.0 / v1.z, p2.y, 1.0 / v2.z)

    ## lighting calculations
    ## calc triangle center
    normal =
    ## compute intensity
    intensity = ComputeLighting(v,normal,v,v)

    # Determine which is left and which is right.
    m = int(len(x02) / 2)
    if x02[m] < x012[m]:
        x_left, x_right = x02, x012
        iz_left, iz_right = iz02, iz012

    else:
        x_left, x_right = x012, x02
        iz_left, iz_right = iz012, iz02

    # Draw horizontal segments.
    for y in range(p0.y, p2.y + 1):
        xl, xr = int(x_left[y - p0.y]), int(x_right[y - p0.y])

        # Interpolate attributes for self scanline.
        zl, zr = iz_left[y - p0.y], iz_right[y - p0.y]
        zscan = interpolate(xl, zl, xr, zr)
        for x in range(xl, xr):
            inv_z = zscan[x - xl]
            if UpdateDepthBufferIfCloser(canvas, depth_buffer, x, y, inv_z):
                putPixel(x, y, triangle.color * intensity, canvas)


def RenderScene(camera, instances, depth_buffer, canvas, lights):
    cameraMatrix = MultiplyMM4(Transposed(camera.orientation), MakeTranslationMatrix(Multiply(-1, camera.position)))

    for i in range(0, len(instances)):
        transform = MultiplyMM4(cameraMatrix, instances[i].transform)
        clipped = TransformAndClip(camera.clipping_planes, instances[i].model, instances[i].scale, transform)
        if (clipped != None):
            RenderModel(clipped, depth_buffer, canvas, lights)


def RenderModel(model, depth_buffer, canvas, lights):
    projected = []
    for i in range(0, len(model.vertices)):
        projected.append(projectVertex(Vertex4(model.vertices[i]), canvas))
    for i in range(0, len(model.triangles)):
        # renderTriangle(model.triangles[i], projected, canvas)
        renderTriangleDepth(model.triangles[i], model.vertices, projected, depth_buffer, canvas, lights)


# Clipping

# Clips a triangle against a plane. Adds output to triangles and vertices.
def ClipTriangle(triangle, plane, triangles, vertices):
    v0 = vertices[triangle.indexes[0]]
    v1 = vertices[triangle.indexes[1]]
    v2 = vertices[triangle.indexes[2]]

    in0 = Dot(plane.normal, v0) + plane.distance > 0
    in1 = Dot(plane.normal, v1) + plane.distance > 0
    in2 = Dot(plane.normal, v2) + plane.distance > 0

    in_count = in0 + in1 + in2
    if (in_count == 0):
        # Nothing to do - the triangle is fully clipped out.
        ...
    elif (in_count == 3):
        # The triangle is fully in front of the plane.
        triangles.append(triangle)
    elif (in_count == 1):
        # The triangle has one vertex in. Output is one clipped triangle.
        ...
    elif (in_count == 2):
        # The triangle has two vertices in. Output is two clipped triangles.
        ...


def TransformAndClip(clipping_planes, model, scale, transform):
    # Transform the bounding sphere, and attempt early discard.
    center = MultiplyMV(transform, Vertex4(model.bounds_center))
    radius = model.bounds_radius * scale
    for p in range(0, len(clipping_planes)):
        distance = Dot(clipping_planes[p].normal, center) + clipping_planes[p].distance
        if (distance < -radius):
            return None

    # Apply modelview transform.
    vertices = []
    for i in range(0, len(model.vertices)):
        vertices.append(MultiplyMV(transform, Vertex4(model.vertices[i])))

    # Clip the entire model against each successive plane.
    triangles = model.triangles.copy()
    for p in range(0, len(clipping_planes)):
        new_triangles = []
        for i in range(0, len(triangles)):
            ClipTriangle(triangles[i], clipping_planes[p], new_triangles, vertices)

        triangles = new_triangles

    return Model(vertices, triangles, center, model.bounds_radius)

def Magnitud(v):
    return math.sqrt(Dot(v,v));
def ComputeLighting (vertex,normal,camera,lights):
    i = 0
    s = 1
    for light in lights:
        if light.type == "ambient":
            i += light.intensity
        elif light.type == "point":
            L = light.vector - vertex
        else:
            L = light.vector

            # Luz difusa
            n_dot_l = Dot(normal, L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l/(Magnitud(normal)*Magnitud(L))

            # Luz especular
            if s != -1:
                R = 2 * normal * Dot(normal, L) - L
                r_dot_v = Dot(R, camera.position)
                if r_dot_v > 0:
                    i += light.intensity * pow(r_dot_v / (Magnitud(R) * Magnitud(camera.position)), s)
    return i




