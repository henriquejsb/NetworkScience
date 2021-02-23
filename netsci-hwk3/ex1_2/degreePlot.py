import sys
from Graph import Graph
import matplotlib.pyplot as plt

def readGraph(filename):
	graph = Graph()
	f = open(filename,"r")
	lines = f.readlines()
	for l in lines:
		auxL = l.strip().split()
		A = int(auxL[0])
		B = int(auxL[1])
		graph.addEdge(A,B)
	return graph


def plotDegreeDistribution(graph,filename):
	graphname = filename.split(".")[0]
	degreeDist = graph.getDegreeDistribution()
	fig, axs = plt.subplots(1,2)
	fig.tight_layout()
	axs = fig.get_axes()
	ax = axs[0]
	x_axis = [i for i in range(len(degreeDist))]
	#ax.scatter(x_axis,degreeDist)
	ax.plot(x_axis,degreeDist, 'o')
	ax.set_xlabel("Degree")
	ax.set_ylabel("Frequency")
	ax.set_title("Degree distribution for " + graphname)
	ax = axs[1]
	#ax.scatter(x_axis,degreeDist)
	ax.plot(x_axis,degreeDist, 'o')
	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_xlabel("Degree")
	ax.set_ylabel("Frequency")
	ax.set_title("Degree distribution for " + graphname + "\n (Log-log scale)")
	plt.savefig(graphname + "_degree_plot.png", bbox_inches='tight',dpi=100)
	#plt.show()


def main():
	if len(sys.argv) != 2:
		print("Usage: python3 degreePlot.py graphfile")
		return 1
	filename = sys.argv[1]
	graph = readGraph(filename)
	plotDegreeDistribution(graph,filename)


if __name__ == '__main__':
	main()