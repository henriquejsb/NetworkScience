import networkx as nx 
import sys


def calculateModularity(graph,communities):
	
	adj_matrix = nx.adjacency_matrix(graph, weight = "value")
	
	modularity = 0
	n_edges =  adj_matrix.sum()/2
	
	i = 0
	for n1 in nx.nodes(graph):
		j = 0
		for n2 in nx.nodes(graph):
			
			if communities[n1] != communities[n2]:
				j += 1
				continue
			
			n1_degree = nx.degree(graph,n1,weight = "value")
			n2_degree = nx.degree(graph,n2,weight = "value")
			
			modularity += adj_matrix[(i,j)] - ((n1_degree * n2_degree) / (2.0 * n_edges))
			
			j += 1

		i += 1 

	modularity = (1.0 / (2 * n_edges)) * modularity
	return modularity


def main():
	if len(sys.argv) != 3:
		print("Usage: python3 modularity.py graphfile attribute")	
		return
	filename = sys.argv[1]
	graph = nx.read_gml(filename)
	attribute = sys.argv[2]
	communities = nx.get_node_attributes(graph,attribute)
	print(calculateModularity(graph,communities))
	return


if __name__ == '__main__':
	main()