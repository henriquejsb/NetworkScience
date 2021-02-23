from graphGen import Graph 
from giantComponent import computeGiantComponent as GC 
import random
import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np



def createFileName(dirname,N,p,i):
	return dirname + "/" + str(N) + "_" + str(p).replace(".","") + "_" + str(i) + ".txt"

def generateGraphs(N,pmin,pmax,step,repetitions,dirname):
	graphs = []
	while round(pmin,5) <= round(pmax,5):
		for i in range(repetitions):
			graph = Graph(N,False)
			graph.generateGraph(pmin)
			giantComponent = GC(graph)
			graph.setGiantComponent(giantComponent)
			#print(giantComponent)
			graphs.append(graph)
			file = open(createFileName(dirname,N,pmin,i),"w")
			file.write(str(graph))
			file.close()
		pmin += step
	return graphs

def plotGC(N,repetitions,dirname,graphs):
	probLabels = []
	means = []
	stdDevs = []
	auxArray = []
	nGraphs = len(graphs)
	j = 0
	prob = graphs[0].getProb()
	probLabels.append(prob)
	for i in range(nGraphs):
		graph = graphs[i]
		if graph.getProb() != prob:
			prob = graph.getProb()
			probLabels.append(prob)
			j += 1
			mean = np.mean(auxArray)
			stdDev = np.std(auxArray)
			means.append(mean)
			#print(mean)
			stdDevs.append(stdDev)
			auxArray = []
		auxArray.append(graph.getGiantComponent() / N)

	mean = np.mean(auxArray)
	#print(mean)
	stdDev = np.std(auxArray)
	means.append(mean)
	stdDevs.append(stdDev)

		
	fig, ax = plt.subplots(figsize=(10, 5))
	#plt.figure()
	ax.errorbar(probLabels, means, yerr = stdDevs, fmt='go--', color = 'blue',  ecolor='b', capthick=2)
	ax.set_title("Mean and std dev. for fraction of nodes in the giant component for graph with \n" + str(N) + " nodes ER model with " + str(repetitions) + " repetitions")
	ax.set_xlabel("Probability for each edge")
	ax.set_ylabel("Average of fraction of nodes in giant component")
	plt.savefig(dirname + '/plot.png')
	plt.show()



def main():
	if len(sys.argv) != 6:
		print("Usage: python3 plotter.py N[size of graph] pmin[minimum prob] pmax[max prob] step repetitions")
		return
	dirname = str(datetime.now().time()).replace(":","_").replace(".","_")
	if not os.path.exists(dirname):
   		os.makedirs(dirname)
	random.seed(0)
	N = int(sys.argv[1])
	pmin = float(sys.argv[2])
	pmax = float(sys.argv[3])
	step = float(sys.argv[4])
	repetitions = int(sys.argv[5])
	graphs = generateGraphs(N,pmin,pmax,step,repetitions,dirname)
	plotGC(N,repetitions, dirname, graphs)
	#plot()

if __name__ == '__main__':
	main()

