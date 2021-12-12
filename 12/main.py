from collections import defaultdict
from copy import copy

edges = defaultdict(list)

with open('task.txt') as f:
# with open('test.txt') as f:
	for line in f.read().splitlines():
		p1, p2 = line.split('-')
		edges[p1].append(p2)
		edges[p2].append(p1)

paths = []

def printAllPathsUtil(u, d, visited, path, lower_twice):

	# Mark the current node as visited and store in path
	visited[u] += 1
	path.append(u)

	# print('RECURING', path, u, lower_twice)

	# if len(path) > 10:
	# 	return

	# If current vertex is same as destination, then print
	# current path[]
	if u == d:
		paths.append(copy(path))
	else:
		# If current vertex is not destination
		# Recur for all the vertices adjacent to this vertex
		for i in edges[u]:
			if i == 'start':
				continue

			lower_twice_recur = lower_twice

			if visited[i]:
				if i.islower():
					if lower_twice:
						lower_twice_recur = False
					else:
						continue

			printAllPathsUtil(i, d, visited, path, lower_twice_recur)
				 
	# Remove current vertex from path[] and mark it as unvisited
	path.pop()
	visited[u] -= 1


# Prints all paths from 's' to 'd'
def printAllPaths(s, d):

	# Mark all the vertices as not visited
	visited = defaultdict(int)

	# Create an array to store paths
	path = []

	# Call the recursive helper function to print all paths
	printAllPathsUtil(s, d, visited, path, True)

# print(edges)
total = 0
printAllPaths('start', 'end')
print(len(paths))