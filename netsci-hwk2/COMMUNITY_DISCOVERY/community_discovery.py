import networkx as nx
from modularity import calculateModularity
import matplotlib.pyplot as plt
import numpy as np
import sys

def plot(values, n_communities ,filename):
	print("Creating plot in " + filename + "_modularity_plot.png")
	x = [i for i in range(len(values))]
	fig, axis = plt.subplots()
	axis.scatter(x,values, color = 'b' , s = 1)
	axis.set_title("Modularity values for network " + filename + "\n (" + str(round(values[-1],4)) + ") - No. Communities = " + str(n_communities))
	axis.set_ylabel("Modularity values")
	axis.set_xlabel("Iterations")
	plt.savefig(filename + "_modularity_plot.png")
	


def get_M(graph):
	adj_matrix = nx.adjacency_matrix(graph, weight = "value")
	return adj_matrix.sum() / 2


def init_communities(graph):
	i = 0
	communities = {}
	nodes_in_communities = {}
	
	for n in nx.nodes(graph):
		communities[n] = i
		nodes_in_communities[i] = [n]
		i += 1
	return communities, nodes_in_communities

def community_discovery_2(graph):
	# I tried to use modularity gain but couldn't get it to work
	n_edges = get_M(graph)

	communities, nodes_in_communities = init_communities(graph)
	
	#best_modularity = -1
	best_modularity = calculateModularity(graph,communities)
	converged = False
	modularity_values = [best_modularity]
	while not converged:
		
		converged = True
		
		for n1 in graph:
			Cn1 = communities[n1]
			best_update = Cn1
			for n2 in graph.neighbors(n1):
				Cn2 = communities[n2]
				if Cn1 == Cn2:
					continue
				communities[n1] = Cn2
				aux_modularity = calculateModularity(graph,communities)
				if aux_modularity > best_modularity:
					best_modularity = aux_modularity
					best_update = Cn2
					converged = False
				modularity_values.append(best_modularity)
				communities[n1] = Cn1
			communities[n1] = best_update
	
	nx.set_node_attributes(graph,communities,"CommunitiesGreedy")
	print("Finished calculating")
	print("-------------------------------------------")
	print("Modularity: " + str(best_modularity))
	print("No. of communities: " + str(len(set(communities.values()))))
	print("-------------------------------------------")
	return modularity_values, len(set(communities.values()))

def main():
	if len(sys.argv) != 2:
		print("Usage: python3 community_discovery.py graphfile.gml")
		return
	filename = sys.argv[1]
	print("\n\nOpening file " + filename)
	graph = nx.read_gml(filename)

	filename = filename.split(".")[0]
	print("Calculating communities for network " + filename)

	modularity_values, n_communities = community_discovery_2(graph)

	plot(modularity_values,n_communities,filename)
	
	print("Saving graph in " + filename+"_sol.gml")
	nx.write_gml(graph,filename+"_sol.gml")


if __name__ == '__main__':
	main()