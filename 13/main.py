import re
from collections import defaultdict


# with open('test.txt') as f:
with open('task.txt') as f:
	points = []
	folds = []

	for line in f.read().splitlines():
		if (m := re.match(r'(\d+),(\d+)', line)):
			points.append((int(m.group(1)), int(m.group(2))))
		elif (m := re.match(r'fold along ([xy])=(\d+)', line)):
			axis = 1 if m.group(1) == 'y' else 0
			folds.append((axis, int(m.group(2))))
		else:
			continue

def fold_apply(page, axis, coord):
	print('applying fold', axis, coord)
	page_new = defaultdict(lambda: defaultdict(bool))

	for x in page:
		for y in page[x]:
			point = [x, y]

			if point[axis] > coord:
				point[axis] = 2 * coord - point[axis]

			page_new[point[0]][point[1]] = True

	return page_new



page = defaultdict(lambda: defaultdict(bool))

for x, y in points:
	page[x][y] = True


def part1(page):
	axis, coord = folds.pop(0)
	page = fold_apply(page, axis, coord)


	total = 0

	for x in page:
		for y in page[x]:
			total += 1

	print('PART 1:', total)

def part2(page):
	while folds:
		axis, coord = folds.pop(0)
		page = fold_apply(page, axis, coord)

	maximum = [0, 0]

	for x in page:
		if x > maximum[0]:
			maximum[0] = x

		for y in page[x]:
			if y > maximum[1]:
				maximum[1] = y

	lines = []

	for x in range(maximum[0] + 1):
		line = ''

		for y in range(maximum[1] + 1):
			if page[x][y]:
				line += '#'
			else:
				line += '.'

		lines.append(line)

	# transpose it
	lines = [''.join(s) for s in zip(*lines)]

	print('\n'.join(lines))

# part1(page)
part2(page)

