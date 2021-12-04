with open('task.txt') as f:
# with open('test.txt') as f:
	lines = f.read().splitlines()

numbers = tuple(int(i) for i in lines[0].split(','))

boards = []

for i in range(2, len(lines), 6):
	board = []

	for line in lines[i:i+5]:
		board.append(tuple(int(i) for i in line.split(' ') if i))

	boards.append(board)

masks = [[[False, False, False, False, False] for i in range(5)] for board in boards]
winners = {i: False for i in range(len(boards))}
first_win = False
last_win = -1
winner_count = 0

def board_score(board, mask):
	score = 0

	for row in range(5):
		for column in range(5):
			if not mask[row][column]:
				score += board[row][column]

	return score


for number in numbers:

	# draw number, update masks
	for index, board in enumerate(boards):
		for row in range(5):
			for column in range(5):
				n = board[row][column]
				if n == number:
					masks[index][row][column] = True


	# check for winner
	for index, mask in enumerate(masks):
		if not winners[index]:
			mask_transposed = list(zip(*mask))

			for row in range(5):
				if all(mask[row]):

					if not winners[index]:
						winners[index] = True
						winner_count += 1
						last_win = index

					if not first_win:
						first_win = True
						print('INDEX', index, 'IS A WINNER', number)
						print('PART 1:', board_score(boards[index], mask) * number)

			for column in range(5):
				if all(mask_transposed[column]):
					if not winners[index]:
						winners[index] = True
						winner_count += 1
						last_win = index

					if not first_win:
						first_win = True
						print('INDEX', index, 'IS A WINNER', number)
						print('PART 1:', board_score(boards[index], mask) * number)

	if winner_count == len(boards):
		index = last_win
		print('INDEX', index, 'IS A LAST WINNER', number)
		print('PART 2:', board_score(boards[index], masks[index]) * number)
		break