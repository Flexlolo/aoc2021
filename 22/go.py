import re
import math
from itertools import product, permutations
from collections import Counter, defaultdict
from copy import copy

lines = []





# with open('task.txt') as f:
with open('test.txt') as f:
# with open('debug.txt') as f:
	for line in f.read().splitlines():
		state, ranges_str = line.split(' ')
		state = +1 if state == 'on' else -1

		ranges = []
		for r in ranges_str.split(','):
			m = re.match(r'\w+=(-?\d+)\.\.(-?\d+)', r)
			ranges.append((int(m.group(1)), int(m.group(2))))

		lines.append((state, tuple(ranges)))


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


def shape_size(shape):
	return math.prod(abs(s[1] - s[0]) + 1 for s in shape)

def clamp(v, vmin, vmax):
	return max(vmin, min(v, vmax))


count = defaultdict(int)


# Counter({(0, 15, 0, 10, 0, 1): 1, 
# 		(10, 30, -10, 20, 0, 1): 1, 
# 		(10, 40, 0, 10, 0, 1): 1, 
# 		(10, 20, 0, 10, 0, 1): 0, 
# 		(10, 15, 0, 10, 0, 1): -1, 
# 		(10, 30, 0, 10, 0, 1): -1})



for i in range(len(lines)):
	print('STEP', i + 1)
	step = defaultdict(int)
	state, shape = lines[i]
	# print('')
	# print('COUNT STATE: ')
	# print(dict(count))
	# print('CHECKING LINE', shape, state)

	for sh, s in count.items():
		# print('SEARCHING IN', sh, s)
		overlap, overlap_area = overlap_ranges(shape, sh)
		overlap_area = tuple(overlap_area)

		if overlap:
			# print('FOUND OVERLAP:', overlap_area)
			# print('WAS', step[overlap_area])
			step[overlap_area] -= s
			# print('BECAME', step[overlap_area])
			# step[overlap_area] = clamp(step[overlap_area], -1, 1)

	if state == +1:
		step[shape] += state
	# print(dict(step))

	for key, value in step.items():
		if key in count:
			count[key] += value
		else:
			count[key] = value


	# count.update(step)
	# print('RESULT:')
	# print(dict(count))


total = 0

for shape, sign in count.items():
	total += sign * shape_size(shape)

print(total)


