import math

import numpy
import numpy as np

import gfxlib as gf
from math import floor
from PIL import Image, ImageDraw

width = 501
height = 501

##############################################################################################

# Definir un lienzo
canvas = Image.new('RGB', (int(width), int(height)), (255, 255, 255))

# Definir Vertices frontales
vAf = gf.Vertex(.5, -0.5, -0.5)
vBf = gf.Vertex(.5, 0.5, -0.5)
vCf = gf.Vertex(-.5, 0.5, -0.5)
vDf = gf.Vertex(-.5, -0.5, -0.5)

# Definir Vertices posteriores
vAb = gf.Vertex(.5, -0.5, 0.5)
vBb = gf.Vertex(.5, 0.5, 0.5)
vCb = gf.Vertex(-.5, 0.5, 0.5)
vDb = gf.Vertex(-.5, -0.5, 0.5)

# Juntar los vertices en una lista
cube_vertices = []
cube_vertices.append(vAf), cube_vertices.append(vBf), cube_vertices.append(vCf), cube_vertices.append(vDf),
cube_vertices.append(vAb), cube_vertices.append(vBb), cube_vertices.append(vCb), cube_vertices.append(vDb)

# Definir los colores
BLUE = (10, 10, 255)
RED = (255, 10, 10)
GREEN = (10, 255, 10)
YELLOW = (238, 232, 170)
PURPLE = (186, 85, 211)
CYAN = (0, 255, 255)

# Definir los triangulos
cube_triangles = [(0, 1, 2, RED), (0, 2, 3, RED), (4, 0, 3, GREEN), (4, 3, 7, GREEN), (5, 4, 7, BLUE), (5, 7, 6, BLUE),
             (1, 5, 6, YELLOW), (1, 6, 2, YELLOW), (4, 5, 1, PURPLE), (4, 1, 0, PURPLE), (2, 6, 7, CYAN),
             (2, 7, 3, CYAN)]

cube = gf.Model(cube_vertices, cube_triangles)

def clipTriangleAgainstPlane(triangles, plane, vertices):
    clipped_triangles = []
    for T in triangles:
        clipped_triangles.append(clipTriangle(T, plane, vertices))
    return clipped_triangles

def clipTriangle (triangle, plane, vertices):
    v0 = vertices[triangle[0]]
    v1 = vertices[triangle[1]]
    v2 = vertices[triangle[2]]

    in0 = np.dot(plane.normal, (v0.x, v0.y, v0.z)) + plane.distance > 0
    in1 = np.dot(plane.normal, (v1.x, v1.y, v1.z)) + plane.distance > 0
    in2 = np.dot(plane.normal, (v2.x, v2.y, v2.z)) + plane.distance > 0

    in_count = in0 + in1 + in2

    if in_count == 0:
        # nothing, the triangle is fully clipped
        return []
    elif in_count == 3:
        # return triangle
        return [triangle]
    elif in_count == 1:
        # triangle has one vertex in, output is one clipped triangle
        in_vertex_index = [in0, in1, in2].index(True)
        out_vertex_index1 = (in_vertex_index + 1) % 3
        out_vertex_index2 = (in_vertex_index + 2) % 3

        in_vertex = vertices[triangle.indexes[in_vertex_index]]
        out_vertex1 = vertices[triangle.indexes[out_vertex_index1]]
        out_vertex2 = vertices[triangle.indexes[out_vertex_index2]]

        clipped_vertex1 = calculateClippedVertex(in_vertex, out_vertex1, plane)
        clipped_vertex2 = calculateClippedVertex(in_vertex, out_vertex2, plane)

        return [gf.Triangle([clipped_vertex1, out_vertex1, out_vertex2], triangle.color)]
    elif in_count == 2:
        # triangle has two vertices in, output is two clipped triangles
        out_vertex_index = [in0, in1, in2].index(False)
        in_vertex_index1 = (out_vertex_index + 1) % 3
        in_vertex_index2 = (out_vertex_index + 2) % 3

        in_vertex1 = vertices[triangle.indexes[in_vertex_index1]]
        in_vertex2 = vertices[triangle.indexes[in_vertex_index2]]
        out_vertex = vertices[triangle.indexes[out_vertex_index]]

        clipped_vertex1 = calculateClippedVertex(in_vertex1, out_vertex, plane)
        clipped_vertex2 = calculateClippedVertex(in_vertex2, out_vertex, plane)

        return [
            gf.Triangle([in_vertex1, in_vertex2, clipped_vertex1], triangle.color),
            gf.Triangle([in_vertex2, clipped_vertex1, clipped_vertex2], triangle.color)
        ]


s2 = math.sqrt(2)

clipping_planes = [
    gf.Plane(gf.Vertex(0,0,1), -1),
    gf.Plane(gf.Vertex(s2,0,s2), 0),
    gf.Plane(gf.Vertex(-s2,0,s2), 0),
    gf.Plane(gf.Vertex(0,-s2,s2), 0),
    gf.Plane(gf.Vertex(0,s2,s2), 0),
]

def calculateClippedVertex(in_vertex, out_vertex, plane):
    t = (plane.distance - np.dot(plane.normal, (in_vertex.x, in_vertex.y, in_vertex.z))) / \
        np.dot(plane.normal, (out_vertex.x - in_vertex.x, out_vertex.y - in_vertex.y, out_vertex.z - in_vertex.z))
    return gf.Vertex(
        in_vertex.x + t * (out_vertex.x - in_vertex.x),
        in_vertex.y + t * (out_vertex.y - in_vertex.y),
        in_vertex.z + t * (out_vertex.z - in_vertex.z)
    )


# Instances
def renderInstance(instance, canvas):
    projected = []
    i = 0
    for V in instance.model.vertices:
        Vn = gf.MultiplyMV(instance.transform, V)
        projected.append(gf.projectVertex(Vn, canvas))
    while i < len(instance.model.triangles):
        gf.renderTriangle(instance.model.triangles[i], projected, canvas)
        i += 1


def renderScene(instances, canvas):
    i = 0
    while i < len(instances):
        renderInstance(instances[i], canvas)
        i += 1


instances = [gf.Instance(cube, gf.Vertex(0, 1.5, 10), gf.Vertex(0, 0, 0),  1)]

for plane in clipping_planes:
    clipped_triangles = []
    for instance in instances:
        for triangle in instance.model.triangles:
            clipped_triangles.extend(clipTriangleAgainstPlane([triangle], plane, instance.model.vertices))
    instances = [gf.Instance(gf.Model([], clipped_triangles), instance.position, instance.orientation, instance.scale) for instance in instances]


renderScene(instances, canvas)

canvas.show()
