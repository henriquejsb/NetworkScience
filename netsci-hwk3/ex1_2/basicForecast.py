from Graph import Graph
from degreePlot import readGraph
import sys

def basicForecast(graph):
	converged = False
	N = graph.getSize()
	nIterations = 0
	while not converged:
		converged = True
		nIterations += 1
		voteUpdates = []
		node = 8
		while node < N:
			if graph.getVote(node) == "Undecided":
				vote = graph.calculateVote(node)

				#print(vote)
				if vote != "Undecided":
					#print("heu")
					voteUpdates.append((node,vote))
					converged = False
			#Little hack to reduce iterations because I know undecided voters will only 
			#be nodes ending in 8 or 9
			node += 1 if node % 10 == 8 else 9
		for update in voteUpdates:
			graph.setVote(update[0],update[1])
	return nIterations


def main():
	if len(sys.argv) != 2:
		print("Usage: python3 degreePlot.py graphfile")
		return 1
	filename = sys.argv[1]
	graph = readGraph(filename)
	#graph.printElectionResults()
	nIterations = basicForecast(graph)
	graph.printElectionResults()
	print("Number of iterations : " + str(nIterations))

if __name__ == '__main__':
	main()
