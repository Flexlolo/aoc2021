from itertools import product

with open('task.txt') as f:
# with open('test.txt') as f:
	lines = [[int(i) for i in line] for line in f.read().splitlines()]

steps = 1000
size = len(lines)

def adjacent_points(x, y):
	for px, py in product([x - 1, x, x + 1], [y - 1, y, y + 1]):
		point = (px, py)

		if point == (x, y):
			continue

		if px < 0 or px >= size:
			continue

		if py < 0 or py >= size:
			continue

		yield point


explosions = 0

for step in range(steps):
	explosions_old = explosions

	for x in range(size):
		for y in range(size):
			lines[x][y] += 1


	queue = [*product(range(size), range(size))]

	while queue:
		point = queue.pop(0)
		px, py = point

		if lines[px][py] > 9:
			explosions += 1
			lines[px][py] = 0

			for (ax, ay) in adjacent_points(px, py):
				# print(ax, ay)
				if lines[ax][ay] == 0:
					continue

				lines[ax][ay] += 1
				queue.append((ax, ay))

	if explosions - explosions_old == size * size:
		print('STEP', step + 1, 'SYNCHRONIZED!')
		break

	print('STEP', step + 1, 'EXPLOSIONS', explosions)

