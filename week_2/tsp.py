from math import sqrt, pow
from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np

def distance_calculator(points):
	matrix = []
	size = len(points)
	for origin in points:
		for destination in points:
			distance = sqrt(pow(origin[0] - destination[0], 2) + pow(origin[1] - destination[1], 2))
			matrix.append(distance)
	matrix = np.array(matrix).reshape(size, size)
	return matrix

def pathfinder(points):
	post_office = list(points[0])
	points.append(tuple(post_office))
	data = distance_calculator(points)
	path, distance = solve_tsp_dynamic_programming(data)
	output = str(points[0])
	passed = 0
	for i in path[1:]:
		passed += data[path[i - 1], path[i]]
		output += f' -> {points[path[i]]}{[passed]}'

	return f'{output} = {passed}'


if __name__ == "__main__":
	points = [(0, 2), (2, 5), (5, 2), (6, 6), (8, 3)]
	print(pathfinder(points))