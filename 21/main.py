import re
from itertools import product
from collections import Counter
from copy import copy
import math

players = []

with open('task.txt') as f:
# with open('test.txt') as f:
	for line in f.read().splitlines():
		m = re.match(r'Player \d+ starting position: (\d+)', line)
		players.append(int(m.group(1)))

score = [0 for player in players]


def part1():
	player = -1
	dice = 0
	steps = 0

	while max(score) < 1000:
		player = (player + 1) % len(players)
		steps += 1

		roll = 0

		for i in range(3):
			dice = (dice) % 100 + 1
			roll += dice

		players[player] = (players[player] + roll - 1) % 10 + 1
		score[player] += players[player]


	print('PART 1:', min(score) * 3 * steps)

def part2():
	player = -1

	dice = [sum(p) for p in product((1,2,3), (1,2,3), (1,2,3))]
	dice = Counter(dice)

	def step(position, score, player, stack = None):
		# print('STEP CALL:')
		# print(position, score, player)
		# print(stack)
		# print('')
		if stack is None:
			stack = []

		player = (player + 1) % len(players)

		total = [0 for player in players]

		for roll, universes in dice.items():
			p = copy(position)
			s = copy(score)

			p[player] = (p[player] + roll - 1) % 10 + 1
			s[player] += p[player]

			if s[player] >= 21:
				result = math.prod(stack + [universes])
				total[player] += result
			else:
				results = step(p, s, player, stack + [universes])
				total = [total[i] + results[i] for i in range(len(players))]

		return total

	print('PART 2:', step(players, score, player))

part2()
# PART 2: [444356092776315, 341960390180808]
# 444356092776315 universes, while player 2 merely wins in 341960390180808
# print(score)