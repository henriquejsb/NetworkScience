from graphGen import Graph
import sys 
import queue
global visited
global counter 

def readGraph(filename):
	file = open(filename,"r")
	lines = file.readlines()
	N = int(lines[0].strip().split()[0])
	graph = Graph(N,False)
	for line in lines[1:]:
		a = int(line.strip().split()[0])
		b = int(line.strip().split()[1])
		graph.addEdge(a-1,b-1)
	return graph


def computeGiantComponent(graph):
	global visited
	global counter
	counter = 0
	N = graph.getSize()
	visited = [False for i in range(N)]
	sizeGiantComponent = 0
	for i in range(N):
		if visited[i]:
			continue
		sizeComponent = BFS(graph,i)
		sizeGiantComponent = max(sizeGiantComponent,sizeComponent)
	return sizeGiantComponent



def BFS(graph,i):
	global visited
	global counter
	nodeQueue = queue.Queue()
	nodeQueue.put(i)
	sizeComponent = 0
	visited[i] = True
	counter += 1
	while not nodeQueue.empty():
		node = nodeQueue.get()
		sizeComponent += 1
		neighbours = graph.getNeighbours(node)
		for neighbour in neighbours:
			if not visited[neighbour]:
				nodeQueue.put(neighbour)
				visited[neighbour] = True
	return sizeComponent

def main():
	if len(sys.argv) != 2:
		print("Usage:python3 giant-component.py filename[file with graph]")
		return
	filename = sys.argv[1]
	global counter
	counter = 0
	graph = readGraph(filename)
	sizeGiantComponent = computeGiantComponent(graph)
	print("Size of giante component: " + str(sizeGiantComponent))
	print("Number of componentes: " + str(counter))


if __name__ == '__main__':
	main()