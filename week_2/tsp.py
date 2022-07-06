from math import sqrt, pow
import numpy as np
from itertools import permutations

# создание матрицы расстояний между точками
def distance_calculator(points: list[tuple]) -> np.array:
	post_office = list(points[0])
	points.append(tuple(post_office))
	matrix = []
	size = len(points)
	for origin in points:
		for destination in points:
			distance = sqrt(pow(origin[0] - destination[0], 2) + pow(origin[1] - destination[1], 2))
			matrix.append(distance)
	matrix = np.array(matrix).reshape(size, size)
	return matrix

# bruteforce перебор дистанций с поиском минимальной
def pathfinder_custom(points: list[tuple], data: np.array) -> list[tuple, float]:
	shortest_solution = [(), 0]
	for i in permutations(range(1, len(points))):
		index_list = (0, *(i), 0)
		distance = 0
		for k, i in enumerate(index_list[1 : ]):
			distance += data[index_list[k], i]
		if distance < shortest_solution[1] or shortest_solution[1] == 0:
			shortest_solution = [index_list, distance]
	return shortest_solution

# хаб сборщик выходных данных
def main(points: list[tuple]) -> str:
	data = distance_calculator(points)
	path, distance = pathfinder_custom(points, data)
	output = str(points[0])
	passed = 0
	for i in path[1:-1]:
		passed += data[path[i - 1], path[i]]
		output += f' -> {points[path[i]]}{[passed]}'

	return f'{output} = {passed}'



if __name__ == "__main__":
	points = [(0, 2), (2, 5), (5, 2), (6, 6), (8, 3)]

	print(main(points))

