from itertools import product
from collections import defaultdict

with open('task.txt') as f:
# with open('test.txt') as f:
	mask, inp = f.read().split('\n\n')
	mask = tuple(1 if char == '#' else 0 for char in mask)

	inp = tuple(tuple(1 if char == '#' else 0 for char in line) for line in inp.split('\n'))


def inp_to_dict(inp):
	inp_dict = {}

	for x in range(len(inp)):
		for y in range(len(inp)):
			inp_dict[(x,y)] = inp[x][y]

	return inp_dict

def adj_points(x, y):
	for dx, dy in product((-1, 0, 1), (-1, 0, 1)):
		yield (x + dx, y + dy)

def display(inp, points=[]):
	lines = []

	d = defaultdict(lambda: defaultdict(int))

	for x, y in inp:
		d[x][y] = inp[(x, y)]


	for x in d:
		s = ['#' if p else '.' for p in d[x].values()]
		lines.append(s)
		

	for x, y in points:
		lines[x][y] = 'X'

	print('\n')
	print('\n'.join(''.join(line) for line in lines))
	print('\n')

def point_enhance(inp, x, y, default: str = '0'):
	n = ''

	for p in adj_points(x, y):
		if p in inp:
			n += str(inp[p])
		else:
			n += default

	n = int(n, 2)
	return mask[n]

def enhance(inp, step, infinity_value: str):
	xs = tuple(k[0] for k in inp)
	ys = tuple(k[1] for k in inp)

	xr = (min(xs), max(xs))
	yr = (min(ys), max(ys))

	out = {}

	for x in range(xr[0] - step, xr[1] + step + 1):
		for y in range(yr[0] - step, yr[1] + step + 1):
			out[(x,y)] = point_enhance(inp, x, y, infinity_value)

	return out

def get_total(inp):
	total = 0

	for pixel in inp.values():
		total += pixel

	return total


inp = inp_to_dict(inp)
display(inp)


def solve(inp, steps: int, debug: bool = False):
	for i in range(steps):
		infinity_value = str(i % 2) if mask[0] else '0'
		inp = enhance(inp, 1, infinity_value)

		if debug:
			display(inp)
		# print(inp.keys())

	return get_total(inp)

print('PART 1:', solve(inp, 2))
print('PART 2:', solve(inp, 50))
