import re
from scipy.spatial.transform import Rotation
from itertools import product
from collections import defaultdict

print('PRECOMPUTING STUFF')


def apply_rotation(point, angles):
	r = Rotation.from_euler('xyz', angles, degrees=True)

	if type(point) is list:
		return [tuple(round(i) for i in r.apply(p)) for p in point]
	else:
		return tuple(round(i) for i in r.apply(point))


def produce_rotations():
	rotations = [*product([0, 90, 180, 270], [0, 90, 180, 270], [0, 90, 180, 270])]

	mapping = {}

	for rotation in rotations:
		rot = apply_rotation((1, 2, 3), rotation)

		if rot not in mapping:
			mapping[rot] = []

		mapping[rot].append(rotation)

	unique_rotations = []

	for r in mapping.values():
		unique_rotations.append(r[0])

	return unique_rotations


rotations = produce_rotations()


beacons = []

with open('task.txt') as f:
# with open('test.txt') as f:
	for line in f.read().splitlines():
		if re.match(r'--- scanner \d+ ---', line):
			beacon = []

		elif line:
			beacon.append(tuple(int(i) for i in line.split(',')))

		else:
			beacons.append(beacon)

	beacons.append(beacon)

print('STARTING WORK')

def point_overlap_max(points1, points2, best_return):
	best = 0
	best_pos = (0, 0, 0)

	vectors = defaultdict(int)

	for p1, p2 in product(points1, points2):
		v = tuple(p2[i] - p1[i] for i in range(3))
		vectors[v] += 1

	for v in vectors:
		if vectors[v] >= best_return:
			return vectors[v], tuple(-v[i] for i in range(3))

	return 0, (0,0,0)


def map_beacons(position, points, mapping):
	stack = []

	for beacon in range(len(beacons)):
		if beacon in mapping:
			continue

		for rotation in rotations:
			beacon_points_rotated = apply_rotation(beacons[beacon], rotation)

			# print('CHECKING OVERLAP WITH', beacon, 'ROTATION = ', rotation)
			overlap, beacon_pos = point_overlap_max(points, beacon_points_rotated, 12)
			# print('OVERLAP COUNT:', overlap)

			if overlap >= 12:
				print('FOUND OVERLAP WITH', beacon)
				pos_abs = tuple(position[i] + beacon_pos[i] for i in range(3))
				mapping[beacon] = (pos_abs, rotation)
				stack.append(beacon)
				break

	return stack

mapping = {0: ((0,0,0), rotations[0])}
stack = [0]

print('STARTED MAPPING BEACONS')
while stack:
	beacon = stack.pop(-1)

	position, rotation = mapping[beacon]
	points = beacons[beacon]
	points = apply_rotation(points, rotation)

	print('LOOKING FOR OVERLAPS OF', beacon)
	stack += map_beacons(position, points, mapping)


print('DONE MAPPING BEACONS')
print(mapping)

final_map = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

for beacon in mapping:
	position, rotation = mapping[beacon]
	points = apply_rotation(beacons[beacon], rotation)

	for point in points:
		p = [position[i] + point[i] for i in range(3)]
		final_map[p[0]][p[1]][p[2]] += 1


total = 0

for x in final_map:
	for y in final_map[x]:
		for z in final_map[x][y]:
			total += 1

print('PART 1:', total)


distance_max = 0

for b1, b2 in product(range(len(beacons)), range(len(beacons))):
	if b1 != b2:
		distance = sum([abs(mapping[b1][0][i] - mapping[b2][0][i]) for i in range(3)])

		if distance > distance_max:
			distance_max = distance

print('PART 2:', distance_max)
