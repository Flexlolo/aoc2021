# with open('test.txt') as f:
with open('task.txt') as f:
	lines = [int(i) for i in f.read().split(',')]


def cost_check(mean: int, fuel_const: bool = True) -> int:
	total = 0

	for crab in lines:
		if fuel_const:
			total += abs(crab - mean)
		else:
			n = abs(crab - mean)
			total += int((n / 2)*(1 + n))

	return total

def solve(fuel_const: bool = True):
	cost_min = None

	for i in range(max(lines) + 1):
		cost = cost_check(i, fuel_const)

		if not cost_min or cost < cost_min:
			cost_min = cost

	return cost_min

print('PART 1:', solve(True))
print('PART 2:', solve(False))
