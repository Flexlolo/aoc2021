import re
import math
from itertools import product, permutations
from collections import defaultdict
import time

lines = []

# with open('task.txt') as f:
with open('test.txt') as f:
	for line in f.read().splitlines():
		state, ranges_str = line.split(' ')
		state = state == 'on'

		ranges = []
		for r in ranges_str.split(','):
			m = re.match(r'\w+=(-?\d+)\.\.(-?\d+)', r)
			ranges.append((int(m.group(1)), int(m.group(2))))
			# x=-20..26
		lines.append((state, tuple(ranges)))

def part1(apply_limit: bool = True):
	# points = set()
	points = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))

	step = 0
	for state, ranges in lines:
		step += 1
		skip = False

		for r in ranges:
			if apply_limit:
				if abs(min(r)) > 50:
					skip = True

		if skip:
			continue

		print('PROCESSING LINE')
		print(state, ranges)

		for x in range(ranges[0][0], ranges[0][1] + 1):
			for y in range(ranges[1][0], ranges[1][1] + 1):
				for z in range(ranges[2][0], ranges[2][1] + 1):
					points[x][y][z] = state
					# if state:
					# 	points.add((x,y,z))
					# else:
					# 	points.discard((x,y,z))

		print('STEP:', step)

	# return len(points)
	total = 0
	for x in points:
		for y in points[x]:
			for z in points[x][y]:
				if points[x][y][z]:
					total += 1

	return total


def overlap_ranges(range1, range2):
	results = []

	for r1, r2 in zip(range1, range2):
		overlap = False
		contains = False
		overlap_range = (0,0)

		for i in range(2):
			if i:
				a, b = r2, r1
			else:
				a, b = r1, r2

			# overlap from left
			if b[0] <= a[0] <= b[1]:
				if a[1] <= b[1]:
					# contains?
					contains = True
					overlap_range = (a[0], a[1])
				else:
					# overlaps?
					overlap_range = (a[0], b[1])
				
				overlap = True
				break

			# overlap from right
			if b[0] <= a[1] <= b[1]:
				if a[0] >= b[0]:
					# contains
					contains = True
					overlap_range = (a[0], a[1])
				else:
					# overlap
					overlap_range = (b[0], a[1])

				overlap = True
				break

		results.append((overlap, overlap_range))

	overlap_all = all(o[0] for o in results)
	overlap = [o[1] for o in results]

	return overlap_all, overlap


def overlap_shapes(shapes):
	area = []

	for shape in shapes:
		if not area:
			area = shape
		else:
			overlap, overlap_area = overlap_ranges(shape, area)

			if overlap:
				area = overlap_area
			else:
				area = []
				break

	return area

def shape_size(shape):
	return math.prod(abs(s[1] - s[0]) + 1 for s in shape)


def part2():
	total = 0
	line = 0

	overlapping = {}
	overlapping_area = {}

	for state, shape in lines:
		shapes = [i for i in range(line) if lines[i][0]]
		
		print('STEP', state, shape)
		print('SHAPES:', shapes)
		if state:
			total += shape_size(shape)
		print(total)

		if shapes:
			# print('DOING STUFF')
			# print('')
			on = 1 if state else 0
			overlap_max = len(shapes)
			# overlap_max = 10

			for j in range(1, overlap_max + 1):
				print(f'{j=}')
				sign = pow(-1, j)
				# print('SIGN:', sign)
				# print('')
				start = time.time()
				p = set(tuple(sorted(s)) for s in permutations(shapes, r=j))
				print('GENERATED PERM IN', time.time() - start)
				
				for s in p:
					s = tuple(sorted(s))
					# print('PERM', s)
					# print('')

					if s not in overlapping:
						process = True

						s_small = tuple(s[i] for i in range(len(s) - 1))
						if s_small in overlapping:
							process = overlapping[s_small]

						if process:
							if s_small in overlapping:
								area = overlap_shapes([overlapping_area[s_small], lines[s[-1]][1]])
							else:
								area = overlap_shapes([lines[i][1] for i in s])

							overlapping[s] = True if area else False
							overlapping_area[s] = area
						else:
							overlapping[s] = False
					
					if overlapping[s]:
						area = overlapping_area[s]
						overlap, overlap_area = overlap_ranges(shape, area)

						if overlap:
							size = shape_size(overlap_area)
							# print("OVERLAP; SIZE +=", size)
							total += sign * size


		if state:
			shapes.append(shape)

		line += 1
		print('STEP:', line, 'RESULT:', total)

	return total


print(part2())