import sys
import random

class Graph:
	def __init__(self,N):
		self.N = N
		
		self.matrix = [[0 for j in range(N)] for i in range(N)]
		self.degreeNodes = []
		

	def addEdge(self,a,b):
		if self.matrix[a][b] == 1:
			return
		self.matrix[a][b] = 1
		self.matrix[b][a] = 1
		self.degreeNodes.append(a)
		self.degreeNodes.append(b)

	def getDegreeDistribution(self):
		degreeDict = {}
		for i in range(self.N):
			degree = 0
			for j in range(self.N):
				if self.matrix[i][j]:
					degree += 1
			degreeDict[degree] = degreeDict.get(degree, 0) + 1
		return degreeDict


	def getNeighbours(self,a):
		return self.nodes[a]

	def getSize(self):
		return self.N

	def __str__(self):
		res = ""
		res += str(self.N) + "\n"
		for i in range(self.N):
			for j in range(self.N):
				if j <= i or self.matrix[i][j] == 0:
					continue
				res += str(i+1) + " " + str(j+1) + "\n"
		return res[:-1]

	
	def generateGraph(self,M0,M):
		self.M0 = M0
		self.M = M
		for i in range(self.M0):
			for j in range(self.M0):
				if i != j:
					self.matrix[i][j] = 1
		self.degreeNodes = [j * (self.M0-1) for j in range(self.M0)]
		M0 = self.M0
		while M0 < self.N:
			M = 0
			while M < self.M:
				neighbour = random.choice(self.degreeNodes)
				if self.matrix[neighbour][M0]:
					continue
				self.addEdge(M0,neighbour)
				M += 1
			M0 += 1

	def clearGraph(self):
		self.nodes = [[] for i in range(N)]


		


def main():
	if len(sys.argv) != 4:
		print('Usage: python3 graphGen.py N[number of nodes] m0[Size of original network]  m[Number of connections per node added]')
		return
	random.seed(1)
	N = int(sys.argv[1])
	M0 = int(sys.argv[2])
	M = int(sys.argv[3])
	graph = Graph(N)
	graph.generateGraph(M0,M)
	print(graph)
	return 0



if __name__ == '__main__':
	main()









