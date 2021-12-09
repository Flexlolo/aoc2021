# with open('test.txt') as f:
with open('task.txt') as f:
	lines = [[int(i) for i in line] for line in f.read().splitlines()]

lowest = []
low_sum = 0

for y in range(len(lines)):
	for x in range(len(lines[y])):
		low = True
		adj = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

		for point in adj:
			px, py = point

			if px < 0 or py < 0:
				continue

			if px >= len(lines[y]) or py >= len(lines):
				continue

			if lines[py][px] <= lines[y][x]:
				low = False
				break

		if low:
			lowest.append((x, y))
			low_sum += 1 + lines[y][x]

print('PART 1:', low_sum)

basins = []

def propagate(x, y, visited = None) -> int:
	if not visited:
		visited = set()

	# print('propagate call:', x, y, lines[y][x], visited)
	visited.add((x, y))

	adj = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
	# print('ADJ:', adj)

	for px, py in adj:
		if px < 0 or py < 0:
			continue

		if px >= len(lines[y]) or py >= len(lines):
			continue

		if lines[py][px] != 9:
			if (px, py) not in visited:
				propagate(px, py, visited)


	return len(visited)


for (x, y) in lowest:
	basins.append(propagate(x, y))

top = sorted(basins)[-3:]
# print(top)
print('PART 2:', top[0] * top[1] * top[2])