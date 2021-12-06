# with open('test.txt') as f:
with open('task.txt') as f:
	lines = [int(i) + 1 for i in f.read().split(',')]

lookup = {}

def simulate(cooldown: int, days: int) -> int:
	if (cooldown, days) not in lookup:
		offspring = []

		start = cooldown
		if start <= days:
			offspring.append(start)
			
			for i in range(1, (days - start) // 7 + 1):
				offspring.append(start + 7 * i)

		count = len(offspring)

		for day in offspring:
			count += simulate(9, days - day)

		lookup[(cooldown, days)] = count
		return count

	else:
		return lookup[(cooldown, days)]

def solve(days: int) -> int:
	total = len(lines)

	for line in lines:
		total += simulate(line, days)

	return total

print('PART 1:', solve(80))
print('PART 2:', solve(256))