import pageRank as pR
import matplotlib.pyplot as plt
import sys

def plot(filename,minBeta,maxBeta,step):
	graph = pR.readGraph(filename)
	N = graph.getSize()
	betas = []
	iterations = []
	ranks = [[] for i in range(N)]
	while minBeta <= maxBeta:
		betas.append(minBeta)
		rks, its = pR.pageRank(graph,minBeta)
		iterations.append(its)
		for n in range(N):
			
			ranks[n].append(rks[n][-1])
		minBeta += step
	fig, axis = plt.subplots(1,2)
	#plt.figure()
	ax = axis[0]
	ax.errorbar(betas, iterations,fmt='o--', color = 'b', capthick = 2)
	ax.set_title("PageRank #iterations \nfor graph " + filename.split(".")[0] )
	ax.set_xlabel("Beta values")
	ax.set_ylabel("Iterations")
	ax = axis[1]
	for n in range(N):
		ax.plot(betas,ranks[n],label = "Node " + str(n+1))	
	ax.set_title("PageRank values \nfor graph " + filename.split(".")[0] )
	ax.set_xlabel("Beta values")
	ax.set_ylabel("PageRank values")
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
	fig.tight_layout()
	plt.savefig(filename.split(".")[0] + "_plot.png", bbox_inches='tight',dpi=100)
	plt.show()
		


def main():
	if len(sys.argv) != 5:
		print('Usage: python3 pageRank.py filename minBeta maxBeta step')
		return
	filename = sys.argv[1]
	minBeta = float(sys.argv[2])
	maxBeta = float(sys.argv[3])
	step = float(sys.argv[4])
	plot(filename,minBeta,maxBeta,step)
	return 0




if __name__ == '__main__':
	main()