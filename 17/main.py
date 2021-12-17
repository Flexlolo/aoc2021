import re

with open('task.txt') as f:
# with open('test.txt') as f:
	m = re.match(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', f.read())
	target = [(int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))]

RANGE_MAX = 500

valid = []

for x in range(1, RANGE_MAX):
	for y in range(-RANGE_MAX, RANGE_MAX):
		vel = [x, y]
		pos = [0, 0]

		while True:
			pos = [pos[i] + vel[i] for i in range(len(pos))]

			if vel[0]:
				vel[0] -= 1

			vel[1] -= 1

			# did we overshoot?
			if pos[0] > target[0][1]:
				break

			if pos[1] < target[1][0]:
				break

			if pos[0] >= target[0][0] and pos[1] <= target[1][1]:
				valid.append((x, y))
				break

part1 = max(v[1] for v in valid)
part1 = (part1 * part1 + part1) / 2
print('PART 1:', part1)
print('PART 2:', len(valid))