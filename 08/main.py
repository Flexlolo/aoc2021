from copy import copy

lines = []

# with open('test.txt') as f:
with open('task.txt') as f:
	for line in f.read().splitlines():
		items = [''.join(sorted(i)) for i in line.split(' ') if i != '|']
		lines.append((items[:10], items[10:]))


def part1():
	total = 0

	for mapping, digits in lines:
		for digit in digits:
			if len(digit) in [2, 3, 4, 7]:
				total += 1

	return total


print('PART 1:', part1())


def mapping_check(mapping, params):
	default = {
		'abcefg': 0,
		'cf': 1,
		'acdeg': 2,
		'acdfg': 3,
		'bcdf': 4,
		'abdfg': 5,
		'abdefg': 6,
		'acf': 7,
		'abcdefg': 8,
		'abcdfg': 9
	}

	escape = {k: str('abcdefg'.index(v)) for k, v in params.items()}
	escaped = {''.join([escape[l] for l in key]): value for key, value in default.items()}
	params_mapping = {''.join(['abcdefg'[int(l)] for l in key]): value for key, value in escaped.items()}
	params_mapping = {''.join(sorted(key)): value for key, value in params_mapping.items()}

	if set(mapping) == set(params_mapping.keys()):
		return (True, params_mapping)

	return (False, None)

def params_bruteforce(mapping, params):
	check = True
	used = set()

	for letter in 'abcdefg':
		if letter not in params or len(params[letter]) != 1:
			check = False
		else:
			used.add(params[letter])

	if check:
		return mapping_check(mapping, params)

	for letter in 'abcdefg':
		if letter not in params or len(params[letter]) > 1:
			if letter not in params:
				options = ''.join(list(set('abcdefg').difference(used)))
			else:
				options = params[letter]

			for option in options:
				if option in used:
					continue

				test_params = copy(params)
				test_params[letter] = option

				result, params_mapping = params_bruteforce(mapping, test_params)

				if result:
					return (result, params_mapping)

			return False, None

def mapping_solve(mapping):
	mapping_length = {
		i: [m for m in mapping if len(m) == i] for i in range(2, 8)
	}

	map_to_digit = {
		1: mapping_length[2][0],
		7: mapping_length[3][0],
		4: mapping_length[4][0],
		8: mapping_length[7][0],
	}

	params = {
		'a': ''.join(list(set(map_to_digit[7]).difference(set(map_to_digit[1])))),
		'b': ''.join(list(set(map_to_digit[4]).difference(set(map_to_digit[1])))),
		'c': ''.join(list(map_to_digit[1])),
		'd': ''.join(list(set(map_to_digit[4]).difference(set(map_to_digit[1])))),
		'f': ''.join(list(map_to_digit[1])),
	}

	_, solution = params_bruteforce(mapping, params) 

	return solution

def part2():
	total = 0

	for mapping, digits in lines:
		solution = mapping_solve(mapping)

		number = ''

		for digit in digits:
			number += str(solution[digit])

		total += int(number)

	return total	

print('PART 2:', part2())
