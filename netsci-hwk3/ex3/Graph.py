
class Graph:
	def __init__(self):
		self.N = 0
		self.adjList = []
		self.states = []
		self.susceptible = 0
		self.infected = 0
		self.recovered = 0
		
	def copy(self,graph):
		self.N = graph.N
		self.adjList = list(graph.adjList)
		self.states = list(graph.states)
		self.susceptible = graph.susceptible
		self.infected = graph.infected
		self.recovered = graph.recovered


	def resizeGraph(self,N):
		for i in range(self.N,N):
			self.adjList.append([]) 
			self.states.append("S")
			self.susceptible += 1
		self.N = N



	def addEdge(self,A,B):
		maxNode = max(A,B) + 1 #Assuming 0 based node IDs
		if maxNode > self.N:
			self.resizeGraph(maxNode)
		self.adjList[A].append(B)
		self.adjList[B].append(A)
		

	def getSize(self):
		return self.N

	def getNeighbours(self,node):
		return self.adjList[node]

	def getState(self,node):
		return self.states[node]


	def setState(self,node,state):
		oldState = self.states[node]

		if oldState == "R":
			self.recovered -= 1
		elif oldState == "S":
			self.susceptible -= 1
		else:
			self.infected -= 1

		self.states[node] = state
		
		if state == "R":
			self.recovered += 1
		elif state == "S":
			self.susceptible += 1
		else:
			self.infected += 1


	def getInfected(self):
		return self.infected

	def getRecovered(self):
		return self.recovered

	def getSusceptible(self):
		return self.susceptible