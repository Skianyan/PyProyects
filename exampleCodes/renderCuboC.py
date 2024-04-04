from PIL import Image,ImageDraw
import graflibC as gf


#Tamaño de la imagen
width=501
height=501

#Definir un lienzo
canvas = Image.new('RGB', (width,height), (255,255,255))

def renderInstance(instance): 
  projected = [ ]
  model = instance.model
  for V in model.vertices:
    Vn = gf.MultiplyMV(gf.model.transform,V)
    instance.projected.append(gf.projectVertex(Vn))
  for i in model.triangles:
    gf.renderTriangle(model.triangles[i], projected)
  


def renderScene(instances):
  for I in instances:
    renderInstance(instances[i])

vertices = [
  gf.Vertex(1, 1, 1),
  gf.Vertex(-1, 1, 1),
  gf.Vertex(-1, -1, 1),
  gf.Vertex(1, -1, 1),
  gf.Vertex(1, 1, -1),
  gf.Vertex(-1, 1, -1),
  gf.Vertex(-1, -1, -1),
  gf.Vertex(1, -1, -1)
];

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

triangles = [
 gf.Triangle((0, 1, 2), RED),
 gf.Triangle((0, 2, 3), RED),
 gf.Triangle((4, 0, 3), GREEN),
 gf.Triangle((4, 3, 7), GREEN),
 gf.Triangle((5, 4, 7), BLUE),
 gf.Triangle((5, 7, 6), BLUE),
 gf.Triangle((1, 5, 6), YELLOW),
 gf.Triangle((1, 6, 2), YELLOW),
 gf.Triangle((4, 5, 1), PURPLE),
 gf.Triangle((4, 1, 0), PURPLE),
 gf.Triangle((2, 6, 7), CYAN),
 gf.Triangle((2, 7, 3), CYAN)
];

cube = gf.Model(vertices, triangles);

instances = [gf.Instance(cube, gf.Vertex(-1.5, 0, 7)),
	         gf.Instance(cube, gf.Vertex(1.25, 2, 7.5))]

renderScene(instances);

canvas.show()
