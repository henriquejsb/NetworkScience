from graphGen import Graph
import sys 
import matplotlib.pyplot as plt
import numpy as np
import powerlaw as pwl

def readGraph(filename):
	file = open(filename,"r")
	lines = file.readlines()
	N = int(lines[0].strip().split()[0])
	graph = Graph(N)
	for line in lines[1:]:
		a = int(line.strip().split()[0])
		b = int(line.strip().split()[1])
		#print(str(a) + " - " + str(b))
		graph.addEdge(a-1,b-1)
		#graph.addEdge(b-1,a-1)
	return graph


def plotDegreeDistribution(filename):
	graph = readGraph(filename)
	
	degreeDict = graph.getDegreeDistribution()
	keys = list(degreeDict.keys())
	keys.sort(reverse = True)
	values = []
	auxValues = []
	for key in keys:
		auxValues += [key] * degreeDict[key]
		values.append(degreeDict[key])
	
	values = np.cumsum(values)

	fit = pwl.Fit(values)
	
	
	print('ALPHA= ' + str(fit.power_law.alpha) + '\nX MIN = ' + str(fit.power_law.xmin))
	
	
	fig, ax = plt.subplots(figsize=(10, 5))
	ax.set_xscale('log')
	ax.set_yscale('log')
	ax.errorbar(keys, values,  fmt='bo', color = 'blue',  ecolor='b', capthick=2)
	ax.set_title("Degree distribution of a B-A network (log-log scale)")
	ax.set_xlabel("Degree")
	ax.set_ylabel("Frequency > x")
	plt.savefig(filename.split(".")[0] + '_plot.png')
	
	

	fit.power_law.plot_pdf(color= 'r',linestyle='--')
	

	ax.set_title("Degree distribution of a B-A network with power law plot \nalpha-1 = " + str(round(fit.power_law.alpha,3)) + " x_min = " + str(fit.power_law.xmin))
	plt.savefig(filename.split(".")[0] + '_plot2.png')
	plt.show()
	


def calcAlpha(values):
	xmin = min(values)
	auxSum = 0
	for val in values:
		auxSum += np.log(val / xmin)
	return 1 + len(values) * pow(auxSum,-1)




def main():
	if len(sys.argv) != 2:
		print("Usage:python3 degreePlotter.py filename[file with graph]")
		return
	filename = sys.argv[1]
	plotDegreeDistribution(filename)
	#printMatrix(matrix)
	


if __name__ == '__main__':
	main()