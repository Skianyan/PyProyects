#SCALE MATRIX
import math, numpy as np
def MultiplyMM4(matA, matB):
	result = Mat4x4([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

	for i in range(0, 4):
		for j in range(0, 4):
			for k in range(0, 4):
				result.data[i][j] += matA.data[i][k]*matB.data[k][j]

	return result
class Mat4x4:
    def __init__(self, data):
        self.data = data

scale = 1
scalemat = Mat4x4([[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]])

identity4x4 = Mat4x4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

result = MultiplyMM4(scalemat,identity4x4)

print(result.data)