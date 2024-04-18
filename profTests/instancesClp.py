from PIL import Image, ImageDraw
import graphlib as gf
import math


def ClipTriangle(triangle, plane, triangles, vertices):
    v0 = vertices[triangle.indexes[0]]
    v1 = vertices[triangle.indexes[1]]
    v2 = vertices[triangle.indexes[2]]

    # Calculate the signed distances from each vertex to the plane
    d0 = gf.Dot(plane.normal, v0) + plane.distance
    d1 = gf.Dot(plane.normal, v1) + plane.distance
    d2 = gf.Dot(plane.normal, v2) + plane.distance

    # Count the number of vertices in front of the plane
    num_front = int(d0 > 0) + int(d1 > 0) + int(d2 > 0)

    if num_front == 0:
        # The triangle is entirely behind the plane, discard it
        return
    elif num_front == 3:
        # The triangle is entirely in front of the plane, keep it
        triangles.append(triangle)
        return
    elif num_front == 1:
        # One vertex is in front of the plane, two are behind
        # Calculate the intersection points of the edges with the plane
        if d0 > 0:
            in_front, behind1, behind2 = v0, v1, v2
        elif d1 > 0:
            in_front, behind1, behind2 = v1, v2, v0
        else:
            in_front, behind1, behind2 = v2, v0, v1

        # Calculate intersection points
        intersection1 = IntersectPlane(in_front, behind1, plane)
        intersection2 = IntersectPlane(in_front, behind2, plane)

        # Create new triangles
        new_triangle1 = gf.Triangle([in_front, intersection1, intersection2], triangle.color)
        triangles.append(new_triangle1)
        return
    elif num_front == 2:
        # Two vertices are in front of the plane, one is behind
        # Calculate the intersection points of the edges with the plane
        if d0 <= 0:
            in_front1, in_front2, behind = v1, v2, v0
        elif d1 <= 0:
            in_front1, in_front2, behind = v2, v0, v1
        else:
            in_front1, in_front2, behind = v0, v1, v2

        # Calculate intersection points
        intersection1 = IntersectPlane(behind, in_front1, plane)
        intersection2 = IntersectPlane(behind, in_front2, plane)

        # Create new triangles
        new_triangle1 = gf.Triangle([behind, intersection1, intersection2], triangle.color)
        new_triangle2 = gf.Triangle([intersection1, in_front1, in_front2], triangle.color)
        triangles.extend([new_triangle1, new_triangle2])
        return


def IntersectPlane(p1, p2, plane):
    # Calculate the t parameter for the intersection point
    t = (plane.distance - gf.Dot(plane.normal, p1)) / gf.Dot(plane.normal, gf.Sub(p2, p1))

    # Calculate the intersection point
    intersection = gf.Add(p1, gf.Multiply(t, gf.Sub(p2, p1)))
    # print(intersection.x, intersection.y, intersection.z)
    return intersection


def TransformAndClip(clipping_planes, model, scale, transform):
    # Transform the bounding sphere, and attempt early discard.
    center = gf.MultiplyMV(transform, gf.Vertex4(model.bounds_center))
    radius = model.bounds_radius * scale
    for p in range(0, len(clipping_planes)):
        distance = gf.Dot(clipping_planes[p].normal, center) + clipping_planes[p].distance
        if (distance < -radius):
            return None

    # Apply modelview transform.
    vertices = []
    for i in range(0, len(model.vertices)):
        vertices.append(gf.MultiplyMV(transform, gf.Vertex4(model.vertices[i])))
    # Clip the entire model against each successive plane.
    triangles = model.triangles.copy()
    for p in range(0, len(clipping_planes)):
        new_triangles = []
        for i in range(0, len(triangles)):
            ClipTriangle(triangles[i], clipping_planes[p], new_triangles, vertices)

        triangles = new_triangles

    return gf.Model(vertices, triangles, center, model.bounds_radius)


def RenderScene(camera, instances, canvas):
    cameraMatrix = gf.MultiplyMM4(gf.Transposed(camera.orientation),
                                  gf.MakeTranslationMatrix(gf.Multiply(-1, camera.position)))

    for i in range(0, len(instances)):
        transform = gf.MultiplyMM4(cameraMatrix, instances[i].transform)
        clipped = TransformAndClip(camera.clipping_planes, instances[i].model, instances[i].scale, transform)
        for t in range(0, len(clipped.triangles)):
            print(clipped.triangles[t].indexes)
        if (clipped != None):
            RenderModel(canvas, clipped)


def RenderModel(canvas, model):
    projected = []
    for i in range(0, len(model.vertices)):
        projected.append(gf.projectVertex(gf.Vertex4(model.vertices[i]), canvas))
    for i in range(0, len(model.triangles)):
        #print(model.triangles[i].indexes)
        # if type(model.triangles[i].indexes[1]) == gf.Vertex:
            # print(model.triangles[i].indexes[1].x)
        gf.renderTriangle(model.triangles[i], projected, canvas)


# Tamaño de la imagen
width = 501
height = 501

# Definir un lienzo
canvas = Image.new('RGB', (width, height), (255, 255, 255))

vertices = [
    gf.Vertex(1, 1, 1),
    gf.Vertex(-1, 1, 1),
    gf.Vertex(-1, -1, 1),
    gf.Vertex(1, -1, 1),
    gf.Vertex(1, 1, -1),
    gf.Vertex(-1, 1, -1),
    gf.Vertex(-1, -1, -1),
    gf.Vertex(1, -1, -1)]

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

triangles = [
    gf.Triangle([0, 1, 2], RED),
    gf.Triangle([0, 2, 3], RED),
    gf.Triangle([4, 0, 3], GREEN),
    gf.Triangle([4, 3, 7], GREEN),
    gf.Triangle([5, 4, 7], BLUE),
    gf.Triangle([5, 7, 6], BLUE),
    gf.Triangle([1, 5, 6], YELLOW),
    gf.Triangle([1, 6, 2], YELLOW),
    gf.Triangle([4, 5, 1], PURPLE),
    gf.Triangle([4, 1, 0], PURPLE),
    gf.Triangle([2, 6, 7], CYAN),
    gf.Triangle([2, 7, 3], CYAN)]

# Definir el modelo de un cubo
cube = gf.Model(vertices, triangles, gf.Vertex(0, 0, 0), math.sqrt(3))

# Hacer 3 instancias del cubo
instances = [gf.Instance(cube, gf.Vertex(-1.5, 0, 4), gf.Identity4x4, 0.75)]

# Parámetros de la cámara
camera = gf.Camera(gf.Vertex(-3, 1, 2), gf.MakeOYRotationMatrix(-30))

s2 = math.sqrt(2)
camera.clipping_planes = [
    gf.Plane(gf.Vertex(0, 0, 1), -1),  # Near
    gf.Plane(gf.Vertex(s2, 0, s2), 0),  # Left
    gf.Plane(gf.Vertex(-s2, 0, s2), 0),  # Right
    gf.Plane(gf.Vertex(0, -s2, s2), 0),  # Top
    gf.Plane(gf.Vertex(0, s2, s2), 0),  # Bottom
]

RenderScene(camera, instances, canvas)

canvas.show()