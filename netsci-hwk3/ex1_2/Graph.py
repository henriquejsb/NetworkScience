from functools import cmp_to_key

def compare(a,b):
	return  b[1] - a[1]

class Graph:
	def __init__(self):
		self.N = 0
		self.degreeList = []
		self.adjList = []
		self.votes = []
		self.A = 0
		self.B = 0
		self.Undecided = 0
		self.sortedDegreeList = None #List of [node,degree] sorted by degree

	def copy(self,graph):
		self.N = graph.N
		self.degreeList = list(graph.degreeList)
		self.adjList = list(graph.adjList)
		self.votes = list(graph.votes)
		self.A = graph.A
		self.B = graph.B
		self.Undecided = graph.Undecided
		self.sortedDegreeList = None


	def resizeGraph(self,N):
		for i in range(self.N,N):
			self.degreeList.append(0) 
			self.adjList.append([]) 
			if i % 10 < 4:
				self.votes.append("A")
				self.A += 1
			elif i % 10 < 8:
				self.votes.append("B")
				self.B += 1
			else:
				self.votes.append("Undecided")
				self.Undecided += 1
		self.N = N

	def printElectionResults(self):
		print("#Voters : " + str(self.N))
		print("A : " + str(self.A))
		print("B : " + str(self.B))
		print("Undecided : " + str(self.Undecided))
		print("WINNER : " + (("A (+" + str(self.A - self.B) + ")") if self.A > self.B else (("B (+" + str(self.B - self.A) + ")") if self.B > self.A else "TIE")))



	def addEdge(self,A,B):
		maxNode = max(A,B) + 1 #Assuming 0 based node IDs
		if maxNode > self.N:
			self.resizeGraph(maxNode)
		self.degreeList[A] += 1
		self.degreeList[B] += 1
		self.adjList[A].append(B)
		self.adjList[B].append(A)
		self.sortedDegreeList = None

	def getSize(self):
		return self.N

	def getDegreeDistribution(self):
		degreeDistribution = [0 for i in range(max(self.degreeList)+1)]
		for d in self.degreeList:
			degreeDistribution[d] += 1
		return degreeDistribution

	def getNeighbours(self,node):
		return self.adjList[node]

	def getVote(self,node):
		return self.votes[node]

	def calculateVote(self,node):
		neighbours = self.adjList[node]
		A = 0
		B = 0
		for n in neighbours:
			if self.votes[n] == "A":
				A += 1
			elif self.votes[n] == "B":
				B += 1
		return "A" if A > B else ("B" if B > A else "Undecided")


	def setVote(self,node,vote):
		oldVote = self.votes[node]
		'''
		if(vote != oldVote):
			if node > 3000 and node < 4000:
				print(str(node) + " : " + oldVote + " -> " + vote)
		'''		
		if oldVote == "A":
			self.A -= 1
		elif oldVote == "B":
			self.B -= 1
		else:
			self.Undecided -= 1
		self.votes[node] = vote
		if vote == "A":
			self.A += 1
		elif vote == "B":
			self.B += 1
		else:
			self.Undecided += 1


	def getVoteDiff(self):
		return self.A - self.B


	def getKHighestDegree(self,K):
		nodes = []
		repeated = False
		lastOccurr = 0
		#print(self.degreeList)
		if not self.sortedDegreeList:
			self.sortedDegreeList = []
			for i,d in enumerate(self.degreeList):
				#print(str(i) + " - " + str(d))
				self.sortedDegreeList.append((i,d))
			self.sortedDegreeList.sort(key = cmp_to_key(compare))
		#print(self.sortedDegreeList[:10])
		for i in range(K):
			nodes.append(self.sortedDegreeList[i][0])
		#print(nodes)
		return nodes


