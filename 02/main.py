# with open('test.txt') as f:
with open('task.txt') as f:
	lines = f.read().splitlines()


def part1(lines):
	pos = [0, 0]

	directions = {
		'down': (1, +1),
		'up': (1, -1),
		'forward': (0, +1),
	}

	for line in lines:
		direction, length = line.split(' ')
		index, multiple = directions[direction]
		# print(multiple)
		pos[index] += int(length) * multiple

	print('PART 1:', pos[0] * pos[1])


def part2(lines):
	pos = [0, 0, 0]

	for line in lines:
		direction, length = line.split(' ')

		if direction == 'down':
			pos[2] += int(length)

		elif direction == 'up':
			pos[2] -= int(length)

		elif direction == 'forward':
			pos[0] += int(length)
			pos[1] += pos[2] * int(length)

	print('PART 2:', pos[0] * pos[1])

part2(lines)