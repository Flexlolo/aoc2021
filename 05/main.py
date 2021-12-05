import re
from collections import defaultdict

point_list = []

# with open('test.txt') as f:
with open('task.txt') as f:
	for line in f.read().splitlines():
		m = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
		coords = [int(i) for i in m.groups()]
		points = [(coords[0], coords[1]), (coords[2], coords[3])]
		point_list.append(points)

def get_count(grid):
	count = 0

	for x in grid:
		for y in grid[x]:
			if grid[x][y] > 1:
				count += 1

	return count

def solve(part2: bool = False):
	grid = defaultdict(lambda: defaultdict(int))

	for points in point_list:	
		diagonal = True

		for i in range(2):
			if points[0][i] == points[1][i]:
				opposite = (i+1) % 2
				start = min(points[0][opposite], points[1][opposite])
				end = max(points[0][opposite], points[1][opposite])

				for j in range(start, end + 1):
					if i == 1:
						x = j
						y = points[0][i]
					else:
						y = j
						x = points[0][i]

					grid[x][y] += 1

				diagonal = False
				break

		if diagonal and part2:
			# 5,5 -> 8,2

			step_x = +1 if points[0][0] < points[1][0] else -1
			step_y = +1 if points[0][1] < points[1][1] else -1

			p = [points[0][0], points[0][1]]

			while tuple(p) != points[1]:
				grid[p[0]][p[1]] +=1
				p[0] += step_x
				p[1] += step_y

			grid[points[1][0]][points[1][1]] +=1

	print('ANSWER:', get_count(grid))


print('PART 1')
solve()
print('PART 2')
solve(True)


