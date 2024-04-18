from PIL import Image, ImageDraw
import graflibC as gf
import math


# Clips a triangle against a plane. Adds output to triangles and vertices.
def ClipTriangle(triangle, plane, triangles, vertices):
    v0 = vertices[triangle.indexes[0]]
    v1 = vertices[triangle.indexes[1]]
    v2 = vertices[triangle.indexes[2]]

    # Determine whether each vertex is inside or outside the plane
    inside = [gf.Dot(plane.normal, v) + plane.distance > 0 for v in (v0, v1, v2)]
    in_count = sum(inside)

    if in_count == 0:
        # If all vertices are outside, the triangle is fully clipped out
        return
    elif in_count == 3:
        # If all vertices are inside, the triangle is not clipped, add it as is
        triangles.append(triangle)
        return
    elif in_count == 1:
        # If one vertex is inside, clip the triangle into one new triangle
        inside_index = inside.index(True)
        outside_index1 = (inside_index + 1) % 3
        outside_index2 = (inside_index + 2) % 3
        inside_vertex = [v0, v1, v2][inside_index]
        outside_vertex1 = [v0, v1, v2][outside_index1]
        outside_vertex2 = [v0, v1, v2][outside_index2]
    elif in_count == 2:
        # If two vertices are inside, clip the triangle into two new triangles
        inside_index1, inside_index2 = [i for i, is_inside in enumerate(inside) if is_inside]
        outside_index = [i for i in range(3) if i not in (inside_index1, inside_index2)][0]
        inside_vertex1 = [v0, v1, v2][inside_index1]
        inside_vertex2 = [v0, v1, v2][inside_index2]
        outside_vertex = [v0, v1, v2][outside_index]

    # Find intersection points between edges and the plane
    intersection_points = []
    if in_count == 1:
        intersection1 = gf.IntersectPlane(plane, inside_vertex, outside_vertex1)
        intersection2 = gf.IntersectPlane(plane, inside_vertex, outside_vertex2)
        intersection_points = [intersection1, intersection2]
    elif in_count == 2:
        intersection1 = gf.IntersectPlane(plane, inside_vertex1, outside_vertex)
        intersection2 = gf.IntersectPlane(plane, inside_vertex2, outside_vertex)
        intersection_points = [intersection1, intersection2]

    # Generate new triangles based on the intersection points
    if len(intersection_points) == 2:
        if in_count == 1:
            for intersection_point in intersection_points:
                if intersection_point not in vertices:
                    vertices.append(
                        intersection_point)  # Add new intersection points to the vertices list if not already present
            new_triangle1 = gf.Triangle([vertices.index(inside_vertex)] +
                                        [vertices.index(intersection_point) for intersection_point in
                                         intersection_points],
                                        triangle.color)
            triangles.append(new_triangle1)
        elif in_count == 2:
            for intersection_point in intersection_points:
                if intersection_point not in vertices:
                    vertices.append(
                        intersection_point)  # Add new intersection points to the vertices list if not already present
            new_triangle1 = gf.Triangle([vertices.index(inside_vertex1),
                                         vertices.index(inside_vertex2),
                                         vertices.index(intersection_points[0])], triangle.color)
            new_triangle2 = gf.Triangle([vertices.index(inside_vertex2),
                                         vertices.index(intersection_points[0]),
                                         vertices.index(intersection_points[1])], triangle.color)
            triangles.extend([new_triangle1, new_triangle2])


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
        if (clipped != None):
            RenderModel(canvas, clipped)


def RenderModel(canvas, model):
    projected = []
    for i in range(0, len(model.vertices)):
        projected.append(gf.projectVertex(gf.Vertex4(model.vertices[i]), canvas))
    for i in range(0, len(model.triangles)):
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
instances = [gf.Instance(cube, gf.Vertex(-1, 1, 2), gf.Identity4x4, 0.75),
             gf.Instance(cube, gf.Vertex(0, -2, 3), gf.Identity4x4, 0.75)]

# Parámetros de la cámara
camera = gf.Camera(gf.Vertex(0, 0, 0), gf.MakeOYRotationMatrix(30))

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
