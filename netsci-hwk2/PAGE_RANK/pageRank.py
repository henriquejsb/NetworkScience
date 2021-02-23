import sys

class Graph:
	def __init__(self,N):
		self.N = N
		self.inEdges = [[] for i in range(N)]
		self.outEdges = [[] for i in range(N)]
		self.pageRanks = [[] for i in range(N)]
		self.used = [False for i in range(N)]
		self.weights = [[-1 for i in range(N)] for i in range(N)]

	def addEdge(self,a,b,w):
		self.outEdges[a].append(b)
		self.inEdges[b].append(a)
		self.weights[a][b] = w
		self.used[a] = True
		self.used[b] = True
		
	def getInEdges(self,node):
		return self.inEdges[node]

	def getDegree(self,node):
		return len(self.outEdges[node])

	def getOutEdges(self,node):
		return self.outEdges[node]

	def getSize(self):
		return self.N


def pageRank(graph,beta,E = 0.00001):
	N = graph.getSize()
	converged = False
	ranks = [[1/N] for i in range(N)]
	iterations = 0
	while not converged:
		error = 0
		iterations += 1
		converged = True
		for node in range(N):
			rJ = 0
			for i in graph.getInEdges(node):
				rI = ranks[i][iterations-1]
				rJ += rI / graph.getDegree(i)
			rJ = (1 - beta)/N + beta * rJ
			error += abs(rJ-ranks[node][iterations-1]) 
			
			ranks[node].append(rJ)
		if error > E:
			converged = False
	return ranks,iterations


def printRanks(ranks):
	N = len(ranks)
	iterations = len(ranks[0])
	print("Iterations: " + str(iterations-1))
	for node in range(N):
		print("Node " + str(node+1), end=":")
		for rank in ranks[node]:
			print("%.5f" % rank, end = " ")
		print("")

def printRanksCSV(ranks):
	N = len(ranks)
	iterations = len(ranks[0])
	#Header for iteration identification
	res = ","
	for it in range(iterations):
		res += "Iteration " + str(it) + ","
	res = res[:-1] + "\n"
	#Lines for each node's rank evolution
	for node in range(N):
		res += "Node " + str(node) + ","
		for rank in ranks[node]:
			res += str(rank) + ","
		res = res[:-1] + "\n"
	print(res)



def readGraph(filename):
	file = open(filename,"r")
	lines = file.readlines()
	N = int(lines[0].strip().split()[0])
	graph = Graph(N)
	for line in lines[1:]:
		a = int(line.strip().split()[0])
		b = int(line.strip().split()[1])
		graph.addEdge(a-1,b-1)
	return graph


	
	
def main():
	if len(sys.argv) != 5:
		print('Usage: python3 pageRank.py filename beta epsilon CSV[Y or N]')
		return
	filename = sys.argv[1]
	beta = float(sys.argv[2])
	epsilon = float(sys.argv[3])
	CSV = True if sys.argv[4] == "Y" else False
	graph = readGraph(filename)
	ranks,iterations = pageRank(graph,beta,epsilon)
	if CSV:
		printRanksCSV(ranks)
	else:
		printRanks(ranks)
	return 0



if __name__ == '__main__':
	main()









