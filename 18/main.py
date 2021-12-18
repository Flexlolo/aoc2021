with open('task.txt') as f:
# with open('test.txt') as f:
	lines = f.read().splitlines()

# print(lines)

lines = [eval(l) for l in lines]


def find_reducable_pair(number, stack=None):
	if stack is None:
		stack = []

	if type(number) is list:
		if len(stack) >= 4:
			return stack

		for i, n in enumerate(number):
			result = find_reducable_pair(n, stack + [i])

			if result:
				return result


def find_reducable_int(number, stack=None):
	if stack is None:
		stack = []

	if type(number) is list:
		for i, n in enumerate(number):
			result = find_reducable_int(n, stack + [i])

			if result:
				return result

	elif number >= 10:
		return stack


def find_reducable(number):
	index = find_reducable_pair(number)

	if not index:
		index = find_reducable_int(number)

	return index


def reduce_number(number):

	def unravel(index):
		n = number

		for i in index:
			n = n[i]

		return n

	done = False

	while not done:
		done = True
		index = find_reducable(number)

		if index:
			done = False

			index_str = ''.join([str(i) for i in index])
			n = unravel(index)
			# print('\n')
			# print(n, index)
			# print(number)

			if type(n) is list:
				pair = n
				n = unravel(index[:-1])
				n[index[-1]] = 0

				for i in range(2):
					search = str((i + 1) % 2)

					# print(f'{i=} {search=}')
					if (side := index_str.rfind(search)) != -1:
						index_side = index[:side]
						n = unravel(index_side)

						if type(n[i]) is int:
							n[i] += pair[i]
						else:
							n = n[i]
							while True:
								if type(n[(i + 1) % 2]) is list:
									n = n[(i + 1) % 2]
								else:
									n[(i + 1) % 2] += pair[i]
									break

			else:
				half = n // 2
				pair = [half, n - half]

				n = unravel(index[:-1])
				n.pop(index[-1])
				n.insert(index[-1], pair)


			# print(number)
			
	return number

def magnitude(number):

	def helper(number):
		if type(number) is list:
			n = [helper(i) for i in number]
			return n[0] * 3 + n[1] * 2
		else:
			return number

	return helper(number)




def part1():
	number = lines[0]

	for i in range(1, len(lines)):
		number = [number, lines[i]]
		# print('ADDING NUMBERS')
		# print(number[0])
		# print('+')
		# print(number[1])
		# print('=')
		number = reduce_number(number)
		# print(number)
		# print('\n')
		# break

	print('PART 1:', magnitude(number))

from itertools import product
from copy import deepcopy

def part2():
	mag_max = 0

	for n1, n2 in product(lines, lines):
		if n1 != n2:
			number = [deepcopy(n1), deepcopy(n2)]

			number = reduce_number(number)
			mag = magnitude(number)

			if mag_max < mag:
				mag_max = mag

	print('PART 2:', mag_max)

part1()
part2()