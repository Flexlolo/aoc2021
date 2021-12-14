from copy import copy
from collections import Counter, defaultdict
import time
import math

# with open('test.txt') as f:
with open('task.txt') as f:
	lines = f.read().splitlines()

def mapping_generate(mapping, rules, pair):
	if pair in rules:
		pairs = (pair[0] + rules[pair], rules[pair] + pair[1])
		mapping[pair] = pairs

		for p in pairs:
			if p not in mapping:
				mapping_generate(mapping, rules, p)


def solve(steps):
	pattern = [c for c in lines[0]]
	rules = dict([line.split(' -> ') for line in lines[2:]])

	mapping = {}

	pairs = defaultdict(int)

	for i in range(len(pattern) - 1):
		pair = pattern[i] + pattern[i + 1]
		mapping_generate(mapping, rules, pair)
		pairs[pair] += 1

	for step in range(steps):
		pairs_new = defaultdict(int)

		for pair in pairs:
			for product in mapping[pair]:
				pairs_new[product] += pairs[pair]

		pairs = pairs_new


	count = defaultdict(int)

	for pair in pairs:
		for letter in pair:
			count[letter] += pairs[pair]

	for letter, value in count.items():
		count[letter] = math.ceil(value / 2)

	count = sorted(count.items(), key=lambda x: x[1], reverse=True)

	return count[0][1] - count[-1][1]

print('PART 1:', solve(10))
print('PART 2:', solve(40))
# part2(10)
