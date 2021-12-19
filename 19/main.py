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

	# for p1, p2 in product(points1, points2):
	for p1_index in range(len(points1) - best_return):
		p1 = points1[p1_index]

		for p2 in points2:
			pos = tuple(p1[i] - p2[i] for i in range(3))
				
			points1_ = tuple(p for p in points1 if p != p1)
			points2_ = tuple(p for p in points2 if p != p2)

			count = 1

			for p1_, p2_ in product(points1_, points2_):
				pos_ = tuple(p1_[i] - p2_[i] for i in range(3))

				if pos_ == pos:
					count += 1

			if count > best:
				best = count
				best_pos = pos

			if count > best_return:
				return best, best_pos

	return best, best_pos



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

# ALREADY COMPUTED FROM PART 1
# mapping = {0: ((0, 0, 0), (0, 0, 0)), 6: ((0, -31, 1119), (90, 180, 270)), 9: ((-1321, 2, -46), (0, 270, 180)), 18: ((-49, -24, -1280), (0, 0, 180)), 31: ((1238, -178, -78), (0, 90, 90)), 1: ((37, -80, -2444), (90, 0, 180)), 36: ((65, 1168, -1208), (0, 90, 0)), 5: ((1130, 1142, -1272), (0, 180, 0)), 8: ((-86, 1149, -2358), (90, 180, 90)), 24: ((-1162, 1081, -1316), (0, 90, 270)), 30: ((40, 2228, -1279), (90, 180, 90)), 15: ((1184, 2246, -1175), (90, 0, 0)), 20: ((-1314, 2341, -1255), (90, 0, 270)), 26: ((-126, 2258, -2504), (0, 270, 180)), 12: ((27, 3540, -2514), (0, 90, 270)), 34: ((-1178, 2303, -2387), (0, 90, 90)), 37: ((1165, 2344, -2394), (0, 180, 180)), 3: ((1209, 1115, -2505), (0, 180, 180)), 27: ((1121, 2312, -3580), (0, 90, 180)), 2: ((1245, 2227, -4750), (0, 0, 90)), 10: ((2404, 2318, -3662), (0, 90, 0)), 4: ((3577, 2304, -3694), (90, 180, 180)), 16: ((3660, 3611, -3682), (0, 270, 0)), 33: ((3615, 2401, -4791), (90, 0, 90)), 7: ((1216, 3439, -4790), (90, 180, 0)), 21: ((1173, 1062, -4865), (90, 0, 90)), 32: ((1211, 2274, -5952), (0, 270, 0)), 11: ((1160, 1099, -6084), (0, 180, 90)), 35: ((-125, 2374, -5970), (0, 0, 180)), 38: ((1116, 3482, -5996), (0, 180, 0)), 25: ((69, 2375, -7236), (90, 180, 180)), 23: ((1261, -21, -2424), (0, 270, 270)), 19: ((2385, 2256, -1269), (0, 90, 90)), 29: ((1254, 2329, 40), (0, 90, 0)), 17: ((3541, 2416, -1333), (0, 90, 180)), 22: ((-1255, 1192, -127), (0, 180, 270)), 28: ((-2357, 1058, -1236), (90, 0, 270)), 13: ((-31, 1180, -3732), (0, 0, 270)), 14: ((-1186, 1025, -3561), (0, 270, 90))}

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
