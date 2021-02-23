import sys
from Graph import Graph
import random
import matplotlib.pyplot as plt
import numpy as np
import time

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



def initInfected(graph,n0Infected,infectedNodes):
	N = graph.getSize()
	infected = 0
	while infected != n0Infected:
		node = random.randint(0,N)
		if graph.getState(node) != "I":
			graph.setState(node,"I")
			infected += 1
			infectedNodes[node] = True




def singleSimulation(graph,probInfection,probRecovery,n0Infected):
	days = 0
	N = graph.getSize()
	infectedNodes = [False for i in range(N)]
	initInfected(graph,n0Infected,infectedNodes)
	Ninfected = [graph.getInfected()]
	Nrecovered = [graph.getRecovered()]
	Nsusceptible = [graph.getSusceptible()]
	NnewInfected = [0]
	newInfected = 0
	newRecovered = 0
	print("Day 0", end = " ")
	print("\t#Susceptible = " + str(graph.getSusceptible()), end = " ")
	print("\t#Infected = " + str(graph.getInfected()) + " (+" + str(newInfected) + ")", end = " ")
	print("\t#Recovered = " + str(graph.getRecovered()) + " (+" + str(newRecovered) + ")")
	graphStates = [infectedNodes]
	infectedByNode = [0 for i in range(N)]
	infectedStates = [infectedByNode]
	
	while days < 100:
		infectedNodes = [False for i in range(N)]
		infectedByNode = [0 for i in range(N)]
		updates = []
		newRecovered = 0
		newInfected = 0
		for node in range(N):
			nodeState = graph.getState(node)
			if nodeState == "I":

				infectedNodes[node] = True
				
				#See if neighbours are infected
				neighbours = graph.getNeighbours(node)
				for neighbour in neighbours:
					if graph.getState(neighbour) == "S":
						#Neighbour can be infected
						prob = random.random()
						if prob < probInfection:
							#Neighbour is infected
							if not infectedNodes[neighbour]:
								infectedNodes[neighbour] = True
								infectedByNode[node] += 1	
							updates.append((neighbour,"I"))
				#See if infected node can recover
				prob = random.random()
				if prob < probRecovery:
					#Infected node is recovered
					updates.append((node,"R"))
			else:
				continue
		for update in updates:
			node = update[0]
			state = update[1]
			if graph.getState(node) != state:
				graph.setState(node,state)
				if state == "I":
					newInfected += 1
				elif state == "R":
					newRecovered += 1
		NnewInfected.append(newInfected)

		Ninfected.append(graph.getInfected())
		Nrecovered.append(graph.getRecovered())
		Nsusceptible.append(graph.getSusceptible())
		days += 1
		print("Day " + str(days), end = " ")
		print("\t#Susceptible = " + str(graph.getSusceptible()), end = " ")
		print("\t#Infected = " + str(graph.getInfected()) + " (+" + str(newInfected) + ")", end = " ")
		print("\t#Recovered = " + str(graph.getRecovered()) + " (+" + str(newRecovered) + ")")

		graphStates.append(infectedNodes)
		infectedStates.append(infectedByNode)
	#R0 at day 6
	a = 0
	b = 0
	day5 = graphStates[5]
	for i in range(len(day5)):
		if day5[i]:
			a += 1
			for j in range(6,len(infectedStates)):
				#print(infectedStates[j][i], end = " ")
				b += infectedStates[j][i]
	print("R0 " + str(b/a))
	R0 = b/a

	peakDay = Ninfected.index(max(Ninfected))
	infectedAtPeakDay = graphStates[peakDay]
	a = 0
	b = 0
	for i in range(len(infectedAtPeakDay)):
		if infectedAtPeakDay[i]:
			a += 1
			for j in range(peakDay+1,len(infectedStates)):
				b += infectedStates[j][i]
	print("R at peak infection day " + str(b/a))
	R = b/a
	return Nsusceptible,Ninfected,Nrecovered, NnewInfected,R0,R


def singleVaccineSimulation(graph,probInfection,probRecovery,n0Infected,vaccineRatio):
	
	N = graph.getSize()
	nodes = [i for i in range(N)]
	Nvaccinated = int(vaccineRatio * N)
	auxNvaccinated = 0
	for i in range(n0Infected):
		infectedNode = random.choice(nodes)
		graph.setState(infectedNode,"I")
		nodes.remove(infectedNode)
	while auxNvaccinated < Nvaccinated and len(nodes) > 0:
		vaccinatedNode = random.choice(nodes)
		graph.setState(vaccinatedNode,"R")
		nodes.remove(vaccinatedNode)
		auxNvaccinated += 1

	days = 0

	
	NnewInfected = [0]
	newInfected = 0
	newRecovered = 0
	print("Day 0", end = " ")
	print("\t#Susceptible = " + str(graph.getSusceptible()), end = " ")
	print("\t#Infected = " + str(graph.getInfected()) + " (+" + str(newInfected) + ")", end = " ")
	print("\t#Recovered = " + str(graph.getRecovered()) + " (+" + str(newRecovered) + ")")
	while graph.getInfected() > 0:
		updates = []
		newRecovered = 0
		newInfected = 0
		for node in range(N):
			nodeState = graph.getState(node)
			if nodeState == "I":
				#See if neighbours are infected
				neighbours = graph.getNeighbours(node)
				for neighbour in neighbours:
					if graph.getState(neighbour) == "S":
						#Neighbour can be infected
						prob = random.random()
						if prob < probInfection:
							#Neighbour is infected
							updates.append((neighbour,"I"))
				#See if infected node can recover
				prob = random.random()
				if prob < probRecovery:
					#Infected node is recovered
					updates.append((node,"R"))
			else:
				continue
		for update in updates:
			node = update[0]
			state = update[1]
			if graph.getState(node) != state:
				graph.setState(node,state)
				if state == "I":
					newInfected += 1
				elif state == "R":
					newRecovered += 1
		NnewInfected.append(newInfected)

		
		days += 1
		print("Day " + str(days), end = " ")
		print("\t#Susceptible = " + str(graph.getSusceptible()), end = " ")
		print("\t#Infected = " + str(graph.getInfected()) + " (+" + str(newInfected) + ")", end = " ")
		print("\t#Recovered = " + str(graph.getRecovered()) + " (+" + str(newRecovered) + ")")

	
	return sum(NnewInfected) + n0Infected


def runSimulation(graphfile,probInfection,probRecovery,n0Infected,K):
	originalGraph = readGraph(graphfile)
	graphname = graphfile.split(".")[0]
	susceptible = []
	infected = []
	recovered = []
	newInfected = []
	r0list = []
	rpeaklist = []
	for k in range(K):
		#Run several simulations
		print("\n\n\t\t----------------------- K = " + str(k+1) + " ---------------\n\n")
		graph = Graph()
		graph.copy(originalGraph)
	
		
		s,i,r,ni,r0,rpeak = singleSimulation(graph,probInfection, probRecovery, n0Infected)
		r0list.append(r0)
		rpeaklist.append(rpeak)
		susceptible.append(s)
		infected.append(i)
		recovered.append(r)
		newInfected.append(ni)

	sMeans = []
	sError = []
	iMeans = []
	iError = []
	rMeans = []
	rError = []
	niMeans = []
	niError = []

	days = len(susceptible[0])
	print("\n\n\t\t-----------------------MEAN VALUES---------------\n\n")
	for day in range(days):
		auxS = []
		auxI = []
		auxR = []
		auxNI = []
		for k in range(K):
			auxS.append(susceptible[k][day])
			auxI.append(infected[k][day])
			auxR.append(recovered[k][day])
			auxNI.append(newInfected[k][day])
		sMeans.append(np.mean(auxS))
		sError.append(np.std(auxS))
		iMeans.append(np.mean(auxI))
		iError.append(np.std(auxI))
		rMeans.append(np.mean(auxR))
		rError.append(np.std(auxR))
		niMeans.append(np.mean(auxNI))
		niError.append(np.std(auxNI))

		print("Day " + str(day), end = " ")
		print("\t#Susceptible = " + str(int(sMeans[day])), end = " ")
		print("\t#Infected = " + str(int(iMeans[day])) + " (+" + str(int(niMeans[day])) + ")", end = " ")
		print("\t#Recovered = " + str(int(rMeans[day])) )

	peakDayNewInfected = niMeans.index(max(niMeans))
	peakDayInfected = iMeans.index(max(iMeans))
	print("Peak number of infected nodes = " + str(iMeans[peakDayInfected]) + " at day " + str(peakDayInfected))
	print("Peak number of NEW infected nodes = " + str(niMeans[peakDayNewInfected]) + " at day " + str(peakDayNewInfected))
	#print("Infected before day 6 = " + str(iMeans[5]))
	#print("New infected on day 6 = " + str(niMeans[6]))
	#R0day6 = (1.0 * niMeans[6]) / iMeans[5]
	print("R0 at day 6 = " + str(np.mean(r0list)))
	RpeakInfected = (1.0 * niMeans[peakDayInfected]) / iMeans[peakDayInfected-1]
	print("Estimated R at day of peak infected nodes = " + str(np.mean(rpeaklist)))
	#RpeakNewInfected = (1.0 * niMeans[peakDayNewInfected]) / iMeans[peakDayNewInfected-1]
	#print("Estimated R at day of peak new infected nodes = " + str(RpeakNewInfected))
	fig, ax = plt.subplots()

	x_axis = [i for i in range(days)]
	ax.errorbar(x_axis,sMeans,yerr = sError, fmt = "-o",color = "blue" , label = "Susceptible", ms = 2)
	ax.errorbar(x_axis,iMeans,yerr = iError, fmt = "-o",color = "red" , label = "Infected", ms = 2)
	ax.errorbar(x_axis,rMeans, yerr = rError, fmt = "-o", color = "green", label = "Recovered", ms = 2)
	ax.errorbar(x_axis,niMeans,yerr = niError, fmt = "--o",color = "palevioletred" , label = "New Cases", ms = 2)

	ax.set_xlabel("Days")
	ax.set_ylabel("Frequency")
	ax.set_title("Evolution of susceptible, infected and recovered for " + graphname + "\n Prob. Infection = " + str(round(probInfection,3)) + \
		"   Prob. Recovery = " + str(round(probRecovery,2)) + "  N0Infected = " + str(n0Infected) + "\n " + str(K) + " repetitions")
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	fig.tight_layout()
	currTime = str(time.time()).replace(".","")
	plt.savefig(graphname + "_" + currTime + "_plot.png")
	#plt.show()
	plt.close(fig)
	fig, ax = plt.subplots()
	ax.errorbar(x_axis,niMeans,yerr = niError, fmt = "-o",color = "red" , label = "New Cases", ms = 2)
	ax.set_xlabel("Days")
	ax.set_ylabel("New cases")
	ax.set_title("New cases per day for " + graphname + "\n Prob. Infection = " + str(round(probInfection,3)) + \
		"   Prob. Recovery = " + str(round(probRecovery,2)) + "  N0Infected = " + str(n0Infected) + "\n " + str(K) + " repetitions")
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	fig.tight_layout()
	plt.savefig(graphname +  "_" + currTime +  "_newcases_plot.png")
	plt.close(fig)
	return sum(niMeans) + n0Infected

def runVaccineSimulation(graphfile,probInfection,probRecovery,n0Infected,K,ratio):
	originalGraph = readGraph(graphfile)
	
	totalInfectedValues = []
	for k in range(K):
		#Run several simulations
		print("\n\n\t\t----------------------- K = " + str(k+1) + " ---------------\n\n")
		graph = Graph()
		graph.copy(originalGraph)
	
		
		totalInfected = singleVaccineSimulation(graph,probInfection, probRecovery, n0Infected, ratio)
		
		totalInfectedValues.append(totalInfected)
	return np.mean(totalInfectedValues), np.std(totalInfectedValues)


def startSimulation(graphfile,probInfection,probRecovery,n0Infected,K,vaccinated):
	totalIvalues = []
	totalIerror = []
	vaccineRatios = [0.05 * i for i in range(21)]
	graphname = graphfile.split(".")[0]
	if vaccinated:
		for ratio in vaccineRatios:
			print("\n\n\t\t----------------------- VACCINATED RATIO = " + str(ratio) + " ---------------\n\n")
			res = runVaccineSimulation(graphfile,probInfection,probRecovery,n0Infected,K,ratio)
			totalIvalues.append(res[0])
			totalIerror.append(res[1])
		fig, ax = plt.subplots()

		ax.errorbar(vaccineRatios,totalIvalues, yerr = totalIerror, fmt = "-o",color = "blue" ,  ms = 2)
		
		ax.set_xlabel("Vaccination ratio")
		ax.set_ylabel("Total infected")
		ax.set_title("Total infected according to vaccination ratio for " + graphname + "\n Prob. Infection = " + str(round(probInfection,3)) + \
			"   Prob. Recovery = " + str(round(probRecovery,2)) + "  N0Infected = " + str(n0Infected) + "\n " + str(K) + " repetitions")
		#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
		fig.tight_layout()
		currTime = str(time.time()).replace(".","")
		plt.savefig(graphname + "_" + currTime + "_vaccination_plot.png")
		plt.close(fig)

	else:
		runSimulation(graphfile,probInfection,probRecovery,n0Infected,K)





def main():
	if len(sys.argv) != 7:
		print("Usage: python3 covidSimulation.py graphfile probInfection probRecovery n0Infected kRepetitions  gammaTesting(Y/N)")
		return 1
	random.seed(0)
	graphfile = sys.argv[1]
	probInfection = eval(sys.argv[2])
	probRecovery = eval(sys.argv[3])
	n0Infected = eval(sys.argv[4])
	K = eval(sys.argv[5])
	vaccination = True if sys.argv[6] == "Y" else False
	startSimulation(graphfile,probInfection,probRecovery,n0Infected,K,vaccination)
	


if __name__ == '__main__':
	main()