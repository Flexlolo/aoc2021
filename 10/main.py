with open('task.txt') as f:
# with open('test.txt') as f:
	lines = f.read().splitlines()

def error_score(line, part2: bool = False):
	char_open = '([{<'
	char_close = ')]}>'

	stack = []

	for char in line:
		if char in char_open:
			stack.append(char_open.index(char))
		else:
			index = stack.pop(-1)

			if char != char_close[index]:
				if part2:
					return 0
				else:
					return [3, 57, 1197, 25137][char_close.index(char)]

	score = 0

	while stack:
		index = stack.pop(-1)

		score *= 5
		score += [1, 2, 3, 4][index]

	return score


print('PART 1:', sum([error_score(line, False) for line in lines]))

scores = [error_score(line, True) for line in lines]
scores = [s for s in scores if s]
scores.sort()
# print(scores)
print('PART 2:', scores[len(scores) // 2])

	