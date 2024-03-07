import math
import gfxlib as gf
import numpy as np
from PIL import Image, ImageDraw


width = 501
height = 501

##########################################################################

# Definir un lienzo
canvas = Image.new('RGB', (int(width), int(height)), (255, 255, 255))

##########################################################################
r=4
h1=r*0.999998764
h2=r*1.61803199
rr=1.618037984*r

cos18=math.cos(math.radians(18))
sin18=math.sin(math.radians(18))
cos54=math.cos(math.radians(54))
sin54=math.sin(math.radians(54))

P1 =( 0.5      , -r      , 0.5     )
P6 =( 0.5      , r       , h1+h2)
P2 =( r*cos18, -r*sin18, 0.5     )
P7 =( -P2[0] , -P2[1]  , P6[2] )
P3 =( r*cos54, r*sin54 , 0.5     )
P8 =( -P3[0] , -P3[1]  , P6[2] )
P4 =( -P3[0] ,  P3[1]  , 0.5     )
P9 =( -P4[0] , -P4[1]  , P6[2] )
P5 =( -P2[0] ,  P2[1]  , 0.5     )
P10=(  P2[0] , -P2[1]  , P6[2] )
P11=( 0.5      , -rr     , h1    )
P12=( P1[0]  , -P11[1] , h2    )
P13=(rr*cos54,-rr*sin54, h2    )
P14=( -P13[0], -P13[1] , h1    )
P15=(rr*cos18,-rr*sin18, h1    )
P16=( -P15[0], -P15[1] , h2    )
P17=( P15[0] , -P15[1] , h2    )
P18=( -P17[0], -P17[1] , h1    )
P19=( P10[0] , -P13[1] , h1    )
P20=( -P19[0], -P19[1] , h2    )

vertices= [
( 0.5      , -r      , 0.5     )
,( 0.5      , r       , h1+h2)
,( r*cos18, -r*sin18, 0.5     )
,( -P2[0] , -P2[1]  , P6[2] )
,( r*cos54, r*sin54 , 0.5     )
,( -P3[0] , -P3[1]  , P6[2] )
,( -P3[0] ,  P3[1]  , 0.5     )
,( -P4[0] , -P4[1]  , P6[2] )
,( -P2[0] ,  P2[1]  , 0.5     )
,(  P2[0] , -P2[1]  , P6[2] )
,( 0.5      , -rr     , h1    )
,( P1[0]  , -P11[1] , h2    )
,(rr*cos54,-rr*sin54, h2    )
,( -P13[0], -P13[1] , h1    )
,(rr*cos18,-rr*sin18, h1    )
,( -P15[0], -P15[1] , h2    )
,( P15[0] , -P15[1] , h2    )
,( -P17[0], -P17[1] , h1    )
,( P10[0] , -P13[1] , h1    )
,( -P19[0], -P19[1] , h2    )]


vtxlist = []
for x in vertices:
    vtxlist.append(gf.Vertex(x[0],x[1],x[2]))

v = vtxlist


#pentagons formed by vertices, assuming they are stored in a list
# pentagons = [(0,1,2,3,4),
#              (0,4,5,6,7),(0,1,9,8,7),(1,2,11,10,9),(2,3,13,12,11),(3,4,5,14,13),
#              (14,5,6,15,16),(6,7,8,16,17),(8,9,10,17,18),(10,1,12,18,19),(12,13,14,15,19),
#              (15,16,17,18,19)]
pentagons = [(v[0],v[1],v[2],v[3],v[4]),(v[0],v[4],v[5],v[6],v[7]),(v[0],v[1],v[9],v[8],v[7]),(v[1],v[2],v[11],v[10],v[9]),
             (v[2],v[3],v[13],v[12],v[11]),(v[3],v[4],v[5],v[14],v[13]),
            (v[14],v[5],v[6],v[15],v[16]),(v[6],v[7],v[8],v[16],v[17]),(v[8],v[9],v[10],v[17],v[18]),(v[10],v[1],v[12],v[18],v[19]),
            (v[12],v[13],v[14],v[15],v[19]),
            (v[15],v[16],v[17],v[18],v[19])]

print(pentagons[0][0].x,pentagons[0][0].y,pentagons[0][0].z)
#gf.renderObject(vertices,triangles,canvas)

gf.renderWireframe(vtxlist,canvas)

canvas.show()