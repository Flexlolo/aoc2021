with open('task.txt') as f:
	lines = [int(i) for i in f.read().splitlines()]

def part1(lines):
	last = None
	increased = 0

	for i in lines:
		if last:
			if i - last > 0:
				increased += 1

		last = i

	print(f'PART 1: {increased}')



def part2(lines):
	increased = 0

	for i, n in enumerate(lines):
		if i + 3 < len(lines):
			if n < lines[i + 3]:
				increased += 1

	print('PART 2:', increased)







part2(lines)