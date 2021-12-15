from collections import defaultdict
from itertools import product

import sys
sys.setrecursionlimit(100_000)

with open('task.txt') as f:
# with open('test.txt') as f:
	lines = tuple(tuple(int(i) for i in line) for line in f.read().splitlines())

# print(lines)

def get_adj(x, y, all_dir = False):
	adj = []

	if x < len(lines) - 1:
		adj.append((x + 1, y))

	if y < len(lines) - 1:
		adj.append((x, y + 1))


	if all_dir:
		if x > 0:
			adj.append((x - 1, y))

		if y > 0:
			adj.append((x, y - 1))

	return adj



def shortest_path(lines, x, y, paths):
	if paths[x][y]:
		return paths[x][y]

	result = 0
	
	adj = get_adj(x, y)

	if not adj:
		result = lines[x][y]
	else:
		results = [shortest_path(lines, p[0], p[1], paths) for p in adj]
		result = min(results) + lines[x][y]

	paths[x][y] = result
	return result

def solve(lines):
	paths = defaultdict(lambda: defaultdict(int))
	n = len(lines)

	print('GENERATING SHORTEST PATHS')
	for x in range(n):
		for y in range(n):
			shortest_path(lines, x, y, paths)


	print('OPTIMIZING SHORTEST PATHS')
	stack = [*product(range(n), range(n))]

	while stack:
		x, y = stack.pop(-1)

		adj = get_adj(x, y, True)

		for px, py in adj:
			if paths[px][py] + lines[x][y] < paths[x][y]:
				# print('NEW OPTIMAL FOR', x, y)
				paths[x][y] = paths[px][py] + lines[x][y]

				for p in adj:
					stack.append(p)

				break

	return paths[0][0] - lines[0][0]




print('PART 1:', solve(lines))

def extend_right(lines):
	# extend to the right
	lines_new = []

	for line in lines:
		line_new = []

		for step in range(5):
			for n in line:
				m = (n - 1 + step) % 9 + 1
				line_new.append(m)

		lines_new.append(tuple(line_new))

	return tuple(lines_new)

def extend_down(lines):
	lines_new = []

	for step in range(5):
		for line in lines:
			line_new = []

			for n in line:
				m = (n - 1 + step) % 9 + 1
				line_new.append(m)

			lines_new.append(tuple(line_new))

	return tuple(lines_new)


lines = extend_down(extend_right(lines))
# print(lines)

print('PART 2:', solve(lines))
