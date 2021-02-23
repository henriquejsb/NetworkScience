import sys
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
from os import listdir
import pandas as pd 
import seaborn as sns


def read_information(file):
	'''
	Reads the raw file as a dictionary:

	{	adjacency_string : {z_score : x , freq : y , sp : z} }
	
	'''
	f = open(file,"r")
	lines = f.readlines()
	glob_info = {}
	sum_z_score = 0
	for line in lines[1:]:
		l = line.strip().split(",")
		info = {}
		info["freq"] = int(l[1])
		if info["freq"] == 1:
			
			info["z_score"] = 0
		else:
			info["z_score"] = float(l[2])
		
		glob_info[l[0][1:-1]] = info
		sum_z_score += pow(info["z_score"],2)
	sum_z_score = math.sqrt(sum_z_score)
	for line in lines[1:]:
		l = line.strip().split(",")
		sg = l[0][1:-1]
	
		glob_info[sg]["sp"] = glob_info[sg]["z_score"]/sum_z_score
	return glob_info


def give_labels(networks):
	'''
	Creates a label correspondence between adjacency matrix strings and a unique ID 
	Returns a dictionary and the size of the subgraphs 
	{ adjacency_string : ID }
	'''
	subgraphs = networks[list(networks.keys())[0]].keys()
	subgraphs_labels = {}
	number = 1
	K = 0
	for sg in subgraphs:
		if not K:
			K = math.sqrt(len(sg))
		subgraphs_labels[sg] = number
		number += 1		
	return subgraphs_labels,K


def read_files():
	'''
	Reads all raw files in the folder
	Parses them all as a dictionary
	networks = { network_name : info}
	Where info is the dictionary returned by read_information
	Final structure will be:
	networks = {
		network_name: {
					001 : { z_score : x , sp : y , freq : z}, 
					010 : ...

						}

	} where "001" represents a adjacency matrix string
	

	'''
	print("Reading networks from raw_xxxxx.txt in current directory...")
	files = [f for f in listdir() if "raw" in f]
	networks = {}
	labels_given = False
	subgraphs_labels = None
	K = 0
	for f in files:
		print("\t" + f)
		#Assumes filename as raw_network.txt
		name = f.split(".")[0].split("_")[1]
		networks[name] = read_information(f)
		if not labels_given:
			subgraphs_labels,K = give_labels(networks)
			labels_given = True
	return networks,subgraphs_labels,K




	


def draw_subgraphs(subgraph_labels, K):
	print("\nDrawing subgraphs and corresponding labels in subgraphs.png\n")
	dim = math.ceil(math.sqrt(len(subgraph_labels.keys())))
	fig, plots = plt.subplots(dim,math.ceil(len(subgraph_labels.keys()) / dim))
	fig.tight_layout()
	plots = fig.get_axes()
	subplot = 0
	for key in subgraph_labels.keys():
		graph = nx.MultiDiGraph()
		#Creates a graph for each subgraph so that I can use the draw function of networkx
		for i in range(len(key)):
			if key[i] == "1":
				#Takes into account the adjacency matrix is represented in a line
				graph.add_edge(i // K, i%K)			
		
		nx.draw_shell(graph, ax = plots[subplot], node_size = 50)
		plots[subplot].title.set_text("Subgraph #" + str(subgraph_labels[key]))
		subplot += 1
	while(subplot <  dim * math.ceil(len(subgraph_labels.keys()) / dim)):
		graph = nx.Graph()
		nx.draw(graph,ax = plots[subplot])
		subplot += 1;

	plt.savefig("subgraphs.png",bbox_inches='tight',dpi=100)


def plot_SP(networks,labels):
	print("\nCreating significance profile plots for all networks")
	fig,ax = plt.subplots()
	names = networks.keys()
	types = ['-']
	markers = ["^",(8,2,0),"v","o","+"]
	i = 0
	aux = np.arange(0,len(networks[list(names)[0]].keys())+1,1)
	plt.xticks(aux)
	for name in names:
		info = networks[name]
		scores = [0 for i in range(len(info.keys()) )]
		x_labels = scores
		'''
		Creates a list of 0's, where each position corresponds to a subgraph. 
		Corresponde is made with the subgraph ID to the list index
		ID's start at 1 so index = label[subgraph]-1

		'''
		for sg in info.keys():
			
			scores[labels[sg]-1] = info[sg]["sp"]
		ax.plot(scores, 'o-', marker = markers[i], linewidth=0.5 , ls = '-', label=name)
		'''
		Stores the list "scores" to avoid re computation of it ahead
		when we are plotting the same things but separated by classes of networks (or sets as they are refered to here)
		
		'''
		networks[name] = (scores,info)
		i = (i+1)%len(markers)

	
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.title("Significance profiles for directed motifs K = 3")
	
	fig.canvas.draw()

	ax.set_xticklabels(["#" + str(i) for i in range(1,len(networks[list(names)[0]][1].keys())+2)])
	print("Saving the plot in SP_profiles.png\n")
	plt.savefig("SP_profiles.png", bbox_inches='tight',dpi=100)



	print("Calculating correlations")
	sets = calculateCorrelations(networks)
	
	fig,axis = plt.subplots(len(sets),1)
	fig.canvas.draw()
	i = 0
	j = 0
	for s in sets:
		ax = axis[i]
		for name in s:
			ax.plot(networks[name][0], 'o-', marker = markers[j], linewidth=0.5 , ls = '-', label=name)
			ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
			ax.set_xticklabels([])
			j = (j+1)%len(markers)
		i += 1
	plt.xticks(aux)
	axis[i-1].set_xticklabels(["#" + str(i) for i in range(1,len(networks[list(names)[0]][1].keys())+1)])
	
	print("\nCreating significance profile plots based on created sets")
	print("Saving the plot in SP_profiles_classes.png")
	plt.savefig("SP_profiles_classes.png",bbox_inches='tight',dpi=100)
	


def calculateCorrelations(networks):
	df = pd.DataFrame()
	names = list(networks.keys())
	for name in names:
		df[name] = networks[name][0]
	corr = df.corr()
	print(corr)
	fig,axis = plt.subplots()

	sns.heatmap(corr,xticklabels = names, yticklabels = names, cmap="YlGnBu")
	print("Saving heatmap of correlation of SP's in heatmap.png")
	plt.savefig("heatmap.png",bbox_inches='tight',dpi=100)
	used = set()
	sets = []
	i = 0
	print("Creating sets of networks based on corr. coef. > 0.65")
	for n1 in names:
		if n1 in used:
			continue
		new_set = [n1]
		for n2 in names:
			if n1 == n2:
				continue
			if n2 in used:
				continue
			if corr[n1][n2] > 0.65:
				new_set.append(n2)
				used.add(n2)
		sets.append(new_set)
		used.add(n1)
	return sets

def main():
	networks,labels,K = read_files()
	draw_subgraphs(labels,K)
	plot_SP(networks,labels)	
	
if __name__ == '__main__':
	main()