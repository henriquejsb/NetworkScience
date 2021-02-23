import sys



def parseCSV(file):
	countries = {}
	languages = {}

	
	f = open(file,"r")
	nodeFile = open("unicode_nodes.csv","w")
	edgeFile = open("unicode_edges.csv","w")

	nodeFile.write("ID,Label,CorL\n")
	edgeFile.write("Source,Target,Weight,PopulationAmmount,Type\n")


	lines = f.readlines()
	for line in lines:
		auxLine = line.split(",")
		countryName = auxLine[0]
		countryID= auxLine[1]
		languageName = auxLine[2]
		languageID = auxLine[3]
		popAmount = auxLine[4]
		popPercent = auxLine[5].strip()
		if countryID not in countries:
			countries[countryID] = countryName
			nodeFile.write('"' + countryID + '","' + countryName + '","C"\n')
		if languageID not in languages:
			languages[languageID] = languageName
			nodeFile.write('"' + languageID + '","' + languageName + '","L"\n')
		edgeFile.write('"' + countryID + '","' + languageID + '",' + popPercent + "," + popAmount + ',"undirected"\n')
	nodeFile.close()
	edgeFile.close()






def main():
	if len(sys.argv) != 2:
		print("Usage: python3 parse_csv.py graph.csv")
		return 1
	file = sys.argv[1]
	parseCSV(file)



if __name__ == '__main__':
	main()