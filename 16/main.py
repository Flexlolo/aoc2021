import math

with open('task.txt') as f:
# with open('test.txt') as f:
	string = f.read()
	packet = int(string, 16)
	packet = bin(packet)[2:].zfill(len(string) * 4)


class Packet:

	TYPE_SUM = 0
	TYPE_PRODUCT = 1
	TYPE_MIN = 2
	TYPE_MAX = 3
	TYPE_VALUE = 4
	TYPE_GT = 5
	TYPE_LT = 6
	TYPE_EQ = 7

	def __init__(self, packet_bits: str):
		self.b = packet_bits
		self.i = 0
		self.subpackets = []

		self.parse()

	def _read(self, length: int, as_int: bool) -> str:
		result = self.b[self.i:self.i + length]
		self.i += length

		if as_int:
			return int(result, 2)

		return result

	def get_length(self):
		return self.i

	def parse(self):
		self.version = self._read(3, True)
		self.type = self._read(3, True)

		# print('PARSING PACKET')
		# print(self.b)
		# print(self.version)
		# print(self.type)
		
		# VALUE
		if self.type == self.TYPE_VALUE:
			bits = ''

			while True:
				part = self._read(5, False)
				bits += part[1:]

				if part[0] == '0':
					break

			self.value = int(bits, 2)

		# OPERATOR
		else:
			self.length_type = self._read(1, True)

			if self.length_type:
				self.length = self._read(11, True)
			else:
				self.length = self._read(15, True)


			# print('OPERATOR TYPE')
			# print('LENGTH TYPE:', self.length_type, 'LENGTH:', self.length)
			total_bits = 0
			total = 0

			while True:
				rem = self.b[self.i:]
				subpacket = Packet(rem)
				self.subpackets.append(subpacket)

				length = subpacket.get_length()
				self.i += length
				total_bits += length
				total += 1

				if self.length_type:
					if total >= self.length:
						break

				else:
					if total_bits >= self.length:
						break

	
	def eval(self):
		if self.type == self.TYPE_VALUE:
			return self.value
		else:
			subp = [p.eval() for p in self.subpackets]

			if self.type == self.TYPE_SUM:
				return sum(subp)

			if self.type == self.TYPE_PRODUCT:
				return math.prod(subp)

			if self.type == self.TYPE_MIN:
				return min(subp)

			if self.type == self.TYPE_MAX:
				return max(subp)

			if self.type == self.TYPE_GT:
				return 1 if subp[0] > subp[1] else 0

			if self.type == self.TYPE_LT:
				return 1 if subp[0] < subp[1] else 0

			if self.type == self.TYPE_EQ:
				return 1 if subp[0] == subp[1] else 0
	
	def __str__(self):
		s = f'[VER {self.version}]'

		if self.type == self.TYPE_VALUE:
			s += f'[VALUE] = {self.value}'

		else:
			s += '[OP] {'
			s += ', '.join([str(p) for p in self.subpackets])
			s += '}'

		return s

	def __repr__(self):
		return self.__str__()


p = Packet(packet)


def versions_sum(p):
	total = p.version

	for subp in p.subpackets:
		total += versions_sum(subp)

	return total

part1 = versions_sum(p)
print('PART 1:', part1)

part2 = p.eval()
print('PART 2:', part2)

