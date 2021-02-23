from Graph import Graph
from degreePlot import readGraph
from basicForecast import basicForecast
import sys
import matplotlib.pyplot as plt




def tvAdvertising(originalGraph):
	voteDiffs = []
	won = False
	for k in range(0,10001,1000):
		graph = Graph()
		graph.copy(originalGraph)
		i = int(k / 100)
		for node in range(3000, 3000 + i):
			graph.setVote(node,"A")
		basicForecast(graph)
		diff = graph.getVoteDiff()
		if not won and diff > 0:
			print("Minimum K for A to win -> " + str(k))
			print("Vote difference at K = " + str(k) + " -> " + str(diff))
			won = True
		voteDiffs.append(diff)

	return voteDiffs


def plotResults(files,results, minK, maxK, jump, filename):
	fig, ax = plt.subplots()
	x_axis = [k for k in range(minK,maxK + 1,jump)]
	ax.set_xticks(x_axis)
	for i in range(len(files)):
		file = files[i]
		result = results[i]

		graphname = file.split(".")[0]
		ax.plot(x_axis,result,"-o",label = graphname)
	ax.plot([min(x_axis),max(x_axis)],[0,0], "--", color = "gray")
	ax.legend(loc="upper left")
	ax.set_xlabel("Money spent in advertising (k)")
	ax.set_ylabel("#Votes for A - #Votes for B")
	ax.set_title("Election results according to advertising investment")
	plt.savefig(filename + ".png")
	#plt.show()




def main():
	if len(sys.argv) < 2:
		print("Usage: python3 tvAdvertising.py graphfile1 [graphfile2, ...]")
		return 1
	graphs = []
	for file in sys.argv[1:]:
		graphs.append(readGraph(file))
	results = []
	i = 1
	for graph in graphs:
		print("--------------" + sys.argv[i] + "----------------")
		results.append(tvAdvertising(graph))
		print("--------------" + ('-' * len(sys.argv[i])) + "----------------\n\n")
		i += 1
	plotResults(sys.argv[1:],results, 0, 10000, 1000, "tvAdvertising_plot")

if __name__ == '__main__':
	main()