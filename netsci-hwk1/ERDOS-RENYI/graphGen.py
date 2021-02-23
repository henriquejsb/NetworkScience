import sys
import random

class Graph:
	def __init__(self,N,directed):
		self.N = N
		self.adjList = [[] for i in range(N)]
		self.directed = directed
		self.giantComponent = 0
		self.p = 0

	def addEdge(self,a,b):
		self.adjList[a].append(b)
		if not self.directed:
			self.adjList[b].append(a)
		

	def getNeighbours(self,a):
		return self.adjList[a]

	def getSize(self):
		return self.N

	def __str__(self):
		res = ""
		res += str(self.N) + "\n"
		for i in range(self.N):
			for j in self.adjList[i]:
				if not self.directed and j < i:
					continue
				res += str(i+1) + " " + str(j+1) + "\n"
		return res[:-1]

	def generateGraph(self,p):
		self.p = p
		for i in range(self.N):
			for j in range(i+1,self.N):
				if j == i:
					continue
				prob = random.random()
				if(prob < p):
					self.addEdge(i,j)

	def clearGraph(self):
		self.adjList = [[] for i in range(N)]

	def setGiantComponent(self,gc):
		self.giantComponent = gc

	def getGiantComponent(self):
		return self.giantComponent

	def getProb(self):
		return self.p


def main():
	if len(sys.argv) != 3:
		print('Usage: python3 ER-graph-gen.py N[number of nodes] p[probability]')
		return
	random.seed(10)
	N = int(sys.argv[1])
	p = float(sys.argv[2])
	graph = Graph(N,False)
	graph.generateGraph(p)
	print(graph)
	return 0



if __name__ == '__main__':
	main()









