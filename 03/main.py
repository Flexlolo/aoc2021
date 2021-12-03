from collections import defaultdict

# with open('test.txt') as f:
with open('task.txt') as f:
	lines = f.read().splitlines()

def map_common(lines):
	count = defaultdict(int)
	bit_length = len(lines[0])

	for bit_index in range(bit_length):
		for line in lines:
			if line[bit_index] == '1':
				count[bit_index] += 1

	common = {k: '1' if v / len(lines) >= 0.5 else '0' for k, v in count.items()}
	return common

def part1(lines):
	common = map_common(lines)
	number_common = ''.join(list(common.values()))
	number_uncommon = number_common.replace('1', 'x').replace('0', '1').replace('x', '0')
	print('PART 1:', int(number_common, 2) * int(number_uncommon, 2))
	
def part2_filter(lines, most_common = True):
	bit_length = len(lines[0])

	for bit_index in range(bit_length):
		common = map_common(lines)
		lines = [line for line in lines if (line[bit_index] == common[bit_index]) == most_common]

		if len(lines) == 1:
			return lines[0]

def part2(lines):
	number_common = part2_filter(lines)
	number_uncommon = part2_filter(lines, False)
	print('PART 2:', int(number_common, 2) * int(number_uncommon, 2))

part1(lines)
part2(lines)